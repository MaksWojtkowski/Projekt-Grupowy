import random
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.day_manager import DayManager
from services.upgrade_shop import UpgradeShop
from services.customer_generator import CustomerGenerator
from services.display_service import DisplayService
from exceptions import BankruptcyException, InsufficientFundsException
from events import EventSystem
from models import Chef, Waiter, Oven, Tables, Ingredients, Marketing as MarketingModel


class GameEngine:

    WIN_THRESHOLD = 5000.0
    STARTING_MONEY = 500.0
    BASE_CUSTOMERS = 10

    def __init__(self):
        self._money = self.STARTING_MONEY
        self._day_manager = DayManager()
        self._upgrade_shop = UpgradeShop()
        self._customer_generator = CustomerGenerator()
        self._display_service = DisplayService()
        self._event_system = EventSystem()
        self._is_running = True
        self._daily_revenue = 0.0

        self._chef = Chef("Marco")
        self._waiter = Waiter("Luigi")
        self._oven = Oven()
        self._tables = Tables()
        self._ingredients = Ingredients()
        self._marketing = MarketingModel()

    @property
    def money(self) -> float:
        return self._money

    @property
    def day(self) -> int:
        return self._day_manager.day_number

    @property
    def is_running(self) -> bool:
        return self._is_running

    @property
    def is_day_active(self) -> bool:
        return self._day_manager.is_day_active

    @property
    def day_manager(self) -> DayManager:
        return self._day_manager

    @property
    def upgrade_shop(self) -> UpgradeShop:
        return self._upgrade_shop

    @property
    def display_service(self) -> DisplayService:
        return self._display_service

    @property
    def daily_revenue(self) -> float:
        return self._daily_revenue

    @property
    def chef(self) -> Chef:
        return self._chef

    @property
    def waiter(self) -> Waiter:
        return self._waiter

    @property
    def oven(self) -> Oven:
        return self._oven

    @property
    def tables(self) -> Tables:
        return self._tables

    @property
    def ingredients(self) -> Ingredients:
        return self._ingredients

    @property
    def marketing(self) -> MarketingModel:
        return self._marketing

    def _sync_levels_from_upgrades(self) -> None:
        chef_upgrade = self._upgrade_shop.get_upgrade("Szkolenie Kucharza")
        if chef_upgrade:
            self._chef.level = chef_upgrade.get_level()

        waiter_upgrade = self._upgrade_shop.get_upgrade("Szkolenie Kelnera")
        if waiter_upgrade:
            self._waiter.level = waiter_upgrade.get_level()

        oven_upgrade = self._upgrade_shop.get_upgrade("Piec")
        if oven_upgrade:
            self._oven.level = oven_upgrade.get_level()

        tables_upgrade = self._upgrade_shop.get_upgrade("Stoliki")
        if tables_upgrade:
            self._tables.level = tables_upgrade.get_level()

        ingredients_upgrade = self._upgrade_shop.get_upgrade("Jakość Składników")
        if ingredients_upgrade:
            self._ingredients.level = ingredients_upgrade.get_level()

        marketing_upgrade = self._upgrade_shop.get_upgrade("Marketing")
        if marketing_upgrade:
            self._marketing.level = marketing_upgrade.get_level()

    def get_oven_level(self) -> int:
        return self._oven.level

    def get_quality_bonus(self) -> float:
        return self._ingredients.get_price_bonus()

    def get_marketing_bonus(self) -> float:
        return self._marketing.get_customer_bonus()

    def get_chef_training_level(self) -> int:
        return self._chef.level

    def get_chef_training_bonus(self) -> float:
        return 1.0 + (self._chef.level - 1) * 0.15

    def get_waiter_training_level(self) -> int:
        return self._waiter.level

    def get_tables_count(self) -> int:
        return self._tables.get_count()

    def start_day(self) -> str:
        if self._day_manager.is_day_active:
            return "Dzień już trwa!"

        self._sync_levels_from_upgrades()
        self._event_system.remove_expired_events(self)

        self._day_manager.start_day()
        self._day_manager.set_max_tables(self.get_tables_count())
        self._daily_revenue = 0.0

        marketing_bonus = self.get_marketing_bonus()
        customer_count = int(self.BASE_CUSTOMERS * marketing_bonus) + random.randint(-2, 3)
        customer_count = max(5, customer_count)

        customers = self._customer_generator.generate_customers(customer_count)

        tables_count = self.get_tables_count()

        print(self._display_service.display_day_start(self._day_manager.day_number, customer_count))
        print(f"Dostępne stoliki: {tables_count}")

        event_message = self._event_system.trigger_random_event(self)
        if event_message:
            print(event_message)
            time.sleep(1.5)

        print("\nRozpoczyna się obsługa klientów...\n")
        time.sleep(1.0)

        customers_to_arrive = list(customers)
        arrival_index = 0

        while arrival_index < len(customers_to_arrive) or self._day_manager.has_customers():
            customers_arrived_this_round = 0
            while arrival_index < len(customers_to_arrive) and (random.random() < 0.6 or not self._day_manager.has_customers()):
                new_customer = customers_to_arrive[arrival_index]
                arrival_index += 1
                customers_arrived_this_round += 1

                if self._day_manager.occupied_tables < tables_count:
                    self._day_manager.add_customer_to_queue(new_customer)
                    print(f"Klient {new_customer.name} zajął stolik i składa zamówienie. (Zajęte stoliki: {self._day_manager.occupied_tables}/{tables_count})")
                else:
                    self._day_manager.reject_customer()
                    print(f"Klient {new_customer.name} odszedł - brak wolnych stolików! (Zajęte stoliki: {self._day_manager.occupied_tables}/{tables_count})")

                time.sleep(random.uniform(0.3, 0.6))

                if customers_arrived_this_round >= 3:
                    break

            if self._day_manager.has_customers():
                result = self._day_manager.process_single_customer(
                    self._chef,
                    self._waiter,
                    self._oven,
                    self._ingredients
                )
                print(result["message"])

                if result["success"]:
                    self._daily_revenue += result["earnings"] + result["tip"]

                time.sleep(random.uniform(0.4, 0.8))

        print("\nWszyscy klienci zostali obsłużeni!")
        time.sleep(0.5)

        return self._finish_day()

    def _finish_day(self) -> str:
        summary = self._day_manager.end_day()
        self._money += summary["total"]

        bills = self.calculate_daily_bills()
        self._money -= bills["total"]

        result = self._day_manager.get_summary()
        result += f"\n\nRACHUNKI:"
        result += f"\n  Czynsz: -{bills['rent']:.2f} zł"
        result += f"\n  Media: -{bills['utilities']:.2f} zł"
        result += f"\n  Składniki: -{bills['ingredients']:.2f} zł"
        result += f"\n  Łącznie rachunki: -{bills['total']:.2f} zł"
        result += f"\n\nStan konta: {self._money:.2f} zł"

        if self._money >= self.WIN_THRESHOLD:
            self._is_running = False
            result += "\n" + self._display_service.display_victory(self._money, self._day_manager.day_number)
        elif self._money <= 0:
            self._is_running = False
            raise BankruptcyException(self._money)

        return result

    def serve_customer(self, count: int = 1) -> str:
        return "Klienci są obsługiwani automatycznie po rozpoczęciu dnia."

    def calculate_daily_bills(self) -> dict:
        base_rent = 50.0
        base_utilities = 30.0
        base_ingredients = 20.0

        rent = base_rent * (1 + (self._tables.level - 1) * 0.2)
        utilities = base_utilities * (1 + (self._oven.level - 1) * 0.15)
        ingredients = base_ingredients * (1 + (self._marketing.level - 1) * 0.1)

        total = rent + utilities + ingredients

        return {
            "rent": rent,
            "utilities": utilities,
            "ingredients": ingredients,
            "total": total
        }

    def end_day(self) -> str:
        return "Dzień kończy się automatycznie po obsłużeniu wszystkich klientów."

    def open_shop(self) -> str:

        return self._upgrade_shop.display_shop(self._money)

    def purchase_upgrade(self, choice: str) -> str:
        try:
            index = int(choice) - 1
            upgrade = self._upgrade_shop.get_upgrade_by_index(index)

            if upgrade is None:
                return "Nieprawidłowy wybór."

            success, cost, message = self._upgrade_shop.purchase_upgrade(upgrade.name, self._money)

            if success:
                self._money -= cost
                return message + f"\nPozostało: {self._money:.2f} zł"
            else:
                return message

        except ValueError:
            return "Wpisz numer ulepszenia."
        except InsufficientFundsException as e:
            return str(e)

    def get_status(self) -> str:
        self._sync_levels_from_upgrades()
        return self._display_service.display_status(
            self._money,
            self._day_manager.day_number,
            self._chef.level,
            self._waiter.level,
            self._oven.level,
            self._day_manager.get_remaining_customers(),
            self._tables.get_count(),
            self._ingredients.level,
            self._marketing.level
        )

    def quit_game(self) -> str:
        self._is_running = False
        return self._display_service.display_goodbye()

    def check_game_over(self) -> bool:
        if self._money <= 0:
            return True
        return False

    def check_victory(self) -> bool:
        return self._money >= self.WIN_THRESHOLD

from typing import List, TYPE_CHECKING
import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Customer

if TYPE_CHECKING:
    from models import Chef, Waiter, Oven, Ingredients


class DayManager:

    def __init__(self):
        self._day_number = 0
        self._daily_earnings = 0.0
        self._daily_penalties = 0.0
        self._daily_tips = 0.0
        self._customers_served = 0
        self._customers_lost = 0
        self._customers_rejected = 0
        self._customers_queue: List[Customer] = []
        self._is_day_active = False
        self._occupied_tables = 0
        self._max_tables = 5

    @property
    def day_number(self) -> int:
        return self._day_number

    @property
    def daily_earnings(self) -> float:
        return self._daily_earnings

    @property
    def daily_tips(self) -> float:
        return self._daily_tips

    @property
    def daily_penalties(self) -> float:
        return self._daily_penalties

    @property
    def customers_served(self) -> int:
        return self._customers_served

    @property
    def customers_lost(self) -> int:
        return self._customers_lost

    @property
    def customers_rejected(self) -> int:
        return self._customers_rejected

    @property
    def occupied_tables(self) -> int:
        return self._occupied_tables

    @property
    def max_tables(self) -> int:
        return self._max_tables

    @property
    def is_day_active(self) -> bool:
        return self._is_day_active

    @property
    def customers_queue(self) -> List[Customer]:
        return self._customers_queue.copy()

    def start_day(self) -> None:
        self._day_number += 1
        self._daily_earnings = 0.0
        self._daily_tips = 0.0
        self._daily_penalties = 0.0
        self._customers_served = 0
        self._customers_lost = 0
        self._customers_rejected = 0
        self._customers_queue = []
        self._is_day_active = True
        self._occupied_tables = 0

    def set_max_tables(self, count: int) -> None:
        self._max_tables = count

    def add_customer_to_queue(self, customer: Customer) -> None:
        self._customers_queue.append(customer)
        self._occupied_tables += 1

    def reject_customer(self) -> None:
        self._customers_rejected += 1


    def process_single_customer(self, chef: 'Chef', waiter: 'Waiter',
                                 oven: 'Oven', ingredients: 'Ingredients') -> dict:
        if not self._customers_queue:
            return {"success": False, "message": "Brak klientów w kolejce"}

        customer = self._customers_queue.pop(0)
        order = customer.order

        total_prep_time = 0.0
        for pizza in order.pizzas:
            base_time = pizza.get_preparation_time()
            total_prep_time += base_time * chef.get_modifier() * oven.get_modifier()

        service_time = waiter.get_service_time()
        total_time = total_prep_time + service_time

        result = {
            "customer": customer,
            "order": order,
            "total_time": total_time,
            "success": False,
            "earnings": 0.0,
            "tip": 0.0,
            "penalty": 0.0,
            "mistake": False,
            "rejected": False,
            "message": ""
        }

        mistake_chance = chef.get_mistake_chance()

        if random.random() < mistake_chance:
            penalty = order.total_price
            self._daily_penalties += penalty
            self._customers_lost += 1
            self._occupied_tables -= 1

            result["mistake"] = True
            result["penalty"] = penalty
            result["message"] = f"POMYŁKA! Kucharz pomylił zamówienie dla {customer.name}! Kara: -{penalty:.2f} zł. Klient zwalnia stolik. (Zajęte stoliki: {self._occupied_tables}/{self._max_tables})"
            return result

        if customer.is_satisfied(total_time):
            order.complete()
            earnings = order.total_price * ingredients.get_price_bonus()
            tip = customer.get_tip(total_time)

            self._daily_earnings += earnings
            self._daily_tips += tip
            self._customers_served += 1
            self._occupied_tables -= 1

            result["success"] = True
            result["earnings"] = earnings
            result["tip"] = tip
            result["message"] = f"Obsłużono {customer.name}: +{earnings:.2f} zł (napiwek: +{tip:.2f} zł). Klient zwalnia stolik. (Zajęte stoliki: {self._occupied_tables}/{self._max_tables})"
        else:
            self._customers_lost += 1
            self._occupied_tables -= 1
            result["message"] = f"Klient {customer.name} wyszedł - zbyt długie oczekiwanie ({total_time:.1f}s > {customer.patience:.1f}s). Stolik zwolniony. (Zajęte stoliki: {self._occupied_tables}/{self._max_tables})"

        return result

    def has_customers(self) -> bool:
        return len(self._customers_queue) > 0

    def get_remaining_customers(self) -> int:
        return len(self._customers_queue)

    def end_day(self) -> dict:
        self._is_day_active = False

        for customer in self._customers_queue:
            self._customers_lost += 1
            self._occupied_tables -= 1
        self._customers_queue = []

        return {
            "day": self._day_number,
            "earnings": self._daily_earnings,
            "tips": self._daily_tips,
            "penalties": self._daily_penalties,
            "total": self._daily_earnings + self._daily_tips - self._daily_penalties,
            "served": self._customers_served,
            "lost": self._customers_lost,
            "rejected": self._customers_rejected
        }

    def get_summary(self) -> str:
        total = self._customers_served + self._customers_lost + self._customers_rejected
        net_earnings = self._daily_earnings + self._daily_tips - self._daily_penalties
        summary = (f"\n{'='*50}\n"
                f"Dzień {self._day_number} zakończony!\n"
                f"{'='*50}\n"
                f"Obsłużono klientów: {self._customers_served}/{total}\n"
                f"Klienci, którzy wyszli: {self._customers_lost}\n")

        if self._customers_rejected > 0:
            summary += f"Brak stolików (odrzuceni): {self._customers_rejected}\n"

        summary += (f"Zarobiono: {self._daily_earnings:.2f} zł\n"
                f"Napiwki: {self._daily_tips:.2f} zł\n")

        if self._daily_penalties > 0:
            summary += f"Kary za pomyłki: -{self._daily_penalties:.2f} zł\n"

        summary += (f"Łącznie: {net_earnings:.2f} zł\n"
                   f"{'='*50}")

        return summary

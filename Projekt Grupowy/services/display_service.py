from typing import Any


class DisplayService:

    def __init__(self):
        pass

    def display_welcome(self) -> str:
        return (f"\n{'='*50}\n"
                f"    SYMULATOR PIZZERII\n"
                f"{'='*50}\n"
                f"Witaj w grze! Zarządzaj swoją pizzerią,\n"
                f"obsługuj klientów i osiągnij stan konta wynoszący 5000 zł aby wygrać grę!\n"
                f"Uważaj - bankructwo oznacza koniec gry.\n"
                f"{'='*50}")

    def display_help(self) -> str:
        return (f"\n{'='*50}\n"
                f"DOSTĘPNE KOMENDY:\n"
                f"{'='*50}\n"
                f"  start    - Rozpocznij nowy dzień (automatyczna obsługa)\n"
                f"  sklep    - Otwórz sklep ulepszeń\n"
                f"  status   - Sprawdź status pizzerii\n"
                f"  pomoc    - Wyświetl tę pomoc\n"
                f"  wyjdz    - Zakończ grę\n"
                f"{'='*50}")

    def display_status(self, money: float, day: int, chef_level: int,
                       waiter_level: int, oven_level: int, customers_today: int,
                       tables_count: int = 5, ingredients_level: int = 1,
                       marketing_level: int = 1) -> str:
        return (f"\n{'='*50}\n"
                f"STATUS PIZZERII - Dzień {day}\n"
                f"{'='*50}\n"
                f"Pieniądze: {money:.2f} zł\n"
                f"Kucharz: Poziom {chef_level}\n"
                f"Kelner: Poziom {waiter_level}\n"
                f"Piec: Poziom {oven_level}\n"
                f"Stoliki: {tables_count}\n"
                f"Jakość składników: Poziom {ingredients_level}\n"
                f"Marketing: Poziom {marketing_level}\n"
                f"Klienci w kolejce: {customers_today}\n"
                f"{'='*50}")

    def display_day_start(self, day: int, customer_count: int) -> str:
        return (f"\n{'='*50}\n"
                f"Dzień {day} — Otwarcie pizzerii!\n"
                f"{'='*50}\n"
                f"Dziś pojawi się {customer_count} klientów.\n"
                f"{'='*50}")

    def display_victory(self, total_money: float, days: int) -> str:
        return (f"\n{'='*50}\n"
                f"    GRATULACJE! WYGRAŁEŚ!\n"
                f"{'='*50}\n"
                f"Twój stan konta przekroczył 5000 zł!\n"
                f"Końcowy stan konta: {total_money:.2f} zł\n"
                f"Liczba dni: {days}\n"
                f"{'='*50}")

    def display_game_over(self, final_balance: float, days: int) -> str:
        return (f"\n{'='*50}\n"
                f"    KONIEC GRY - BANKRUCTWO\n"
                f"{'='*50}\n"
                f"Twoja pizzeria zbankrutowała!\n"
                f"Końcowy bilans: {final_balance:.2f} zł\n"
                f"Przetrwałeś {days} dni.\n"
                f"{'='*50}")

    def display_goodbye(self) -> str:
        return (f"\n{'='*50}\n"
                f"Dziękujemy za grę!\n"
                f"{'='*50}")

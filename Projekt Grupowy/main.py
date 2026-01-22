import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from typing import List
from routing import Route, Router
from services import GameEngine, DisplayService
from exceptions import (
    PizzeriaException,
    BankruptcyException,
    RouteNotFoundException,
    InsufficientFundsException
)


def create_routes() -> List[Route]:
    return [
        Route("start", "StartDayAction"),
        Route("sklep", "ShopAction"),
        Route("kup", "ShopAction", "purchase"),
        Route("status", "StatusAction"),
        Route("pomoc", "HelpAction"),
        Route("help", "HelpAction"),
        Route("wyjdz", "QuitAction"),
        Route("quit", "QuitAction"),
    ]


def parse_command(input_line: str) -> tuple:
    parts = input_line.strip().split()
    if not parts:
        return "", []

    command = parts[0]
    args = parts[1:] if len(parts) > 1 else []

    return command, args


def run_shop_mode(game_engine: GameEngine) -> None:
    while True:
        print(game_engine.open_shop())

        try:
            user_input = input("\nWybór: ").strip()

            if user_input.lower() in ['wyjdz', 'exit', 'q', '0']:
                print("Wychodzisz ze sklepu.")
                break

            result = game_engine.purchase_upgrade(user_input)
            print(result)

        except KeyboardInterrupt:
            print("\nWychodzisz ze sklepu.")
            break


def run_game() -> None:
    game_engine = GameEngine()
    routes = create_routes()
    router = Router(routes, game_engine)
    display_service = DisplayService()

    print(display_service.display_welcome())
    print(display_service.display_help())

    while game_engine.is_running:
        try:
            user_input = input("\n> ").strip()

            if not user_input:
                continue

            command, args = parse_command(user_input)

            if command.lower() == 'sklep':
                run_shop_mode(game_engine)
                continue

            try:
                result = router.dispatch(command, *args)

                if result == "__QUIT__":
                    print(game_engine.quit_game())
                    break

                if result:
                    print(result)

            except RouteNotFoundException:
                print(f"Nieznana komenda: '{command}'. Wpisz 'pomoc' aby zobaczyć dostępne komendy.")

        except BankruptcyException as e:
            print(display_service.display_game_over(e.final_balance, game_engine.day))
            break
        except InsufficientFundsException as e:
            print(f"Błąd: {e}")
        except PizzeriaException as e:
            print(f"Błąd: {e}")
        except KeyboardInterrupt:
            print("\n" + game_engine.quit_game())
            break
        except EOFError:
            print("\n" + game_engine.quit_game())
            break


if __name__ == "__main__":
    run_game()

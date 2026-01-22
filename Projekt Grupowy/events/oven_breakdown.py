import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from events.random_event import RandomEvent


class OvenBreakdown(RandomEvent):

    def __init__(self):
        super().__init__(
            name="Awaria Pieca",
            description="Piec w kuchni sie zepsul",
            occurrence_chance=0.08
        )
        self._original_oven_level = 1

    def trigger(self, game_engine) -> str:
        self._is_active = True
        self._original_oven_level = game_engine.oven.level
        self.apply_effect(game_engine)

        return (f"\n{'='*50}\n"
                f"ZDARZENIE: {self._name}\n"
                f"{'='*50}\n"
                f"Twoj piec sie zepsul!\n"
                f"Szybkosc pieczenia spadla do poziomu 1 na ten dzien.\n"
                f"{'='*50}")

    def apply_effect(self, game_engine) -> None:
        game_engine.oven.level = 1
        oven_upgrade = game_engine.upgrade_shop.get_upgrade("Piec")
        if oven_upgrade:
            oven_upgrade._level = 1

    def remove_effect(self, game_engine) -> None:
        game_engine.oven.level = self._original_oven_level
        oven_upgrade = game_engine.upgrade_shop.get_upgrade("Piec")
        if oven_upgrade:
            oven_upgrade._level = self._original_oven_level
        self._is_active = False

import random
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from events.random_event import RandomEvent


class SanitaryInspection(RandomEvent):

    def __init__(self):
        super().__init__(
            name="Inspekcja Sanitarna",
            description="Inspektor zjawil sie w restauracji",
            occurrence_chance=0.10
        )
        self._fine = 0.0

    def trigger(self, game_engine) -> str:
        self._is_active = True
        self._fine = random.uniform(50.0, 150.0)
        self.apply_effect(game_engine)

        return (f"\n{'='*50}\n"
                f"ZDARZENIE: {self._name}\n"
                f"{'='*50}\n"
                f"Inspekcja sanitarna w Twojej restauracji!\n"
                f"Kara: -{self._fine:.2f} zl\n"
                f"{'='*50}")

    def apply_effect(self, game_engine) -> None:
        game_engine._money -= self._fine

    def remove_effect(self, game_engine) -> None:
        self._is_active = False
        self._fine = 0.0

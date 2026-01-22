from .base_upgrade import BaseUpgrade


class WaiterTraining(BaseUpgrade):

    def __init__(self):
        super().__init__(name="Szkolenie Kelnera", base_cost=120.0, max_level=5)

    def get_effect_description(self) -> str:
        return f"Szybkosc obslugi: +{(self.get_bonus() - 1) * 100:.0f}%"

    def get_bonus(self) -> float:
        return 1.0 + (self._level - 1) * 0.2

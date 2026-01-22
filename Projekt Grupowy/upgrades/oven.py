from .base_upgrade import BaseUpgrade


class Oven(BaseUpgrade):

    def __init__(self):
        super().__init__(name="Piec", base_cost=200.0, max_level=5)

    def get_effect_description(self) -> str:
        return f"Szybkość pieczenia: +{(self.get_bonus() - 1) * 100:.0f}%"

    def get_bonus(self) -> float:
        return 1.0 + (self._level - 1) * 0.2

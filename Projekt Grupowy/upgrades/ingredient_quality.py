from .base_upgrade import BaseUpgrade


class IngredientQuality(BaseUpgrade):

    def __init__(self):
        super().__init__(name="Jakość Składników", base_cost=120.0, max_level=5)

    def get_effect_description(self) -> str:
        return f"Bonus do ceny pizz: +{(self.get_bonus() - 1) * 100:.0f}%"

    def get_bonus(self) -> float:
        return 1.0 + (self._level - 1) * 0.1

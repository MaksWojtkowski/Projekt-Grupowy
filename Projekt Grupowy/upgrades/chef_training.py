from .base_upgrade import BaseUpgrade


class ChefTraining(BaseUpgrade):

    def __init__(self):
        super().__init__(name="Szkolenie Kucharza", base_cost=150.0, max_level=5)

    def get_effect_description(self) -> str:
        return f"Umiejętności kucharza: +{(self.get_bonus() - 1) * 100:.0f}%"

    def get_bonus(self) -> float:
        return 1.0 + (self._level - 1) * 0.15

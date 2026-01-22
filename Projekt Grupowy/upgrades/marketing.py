from .base_upgrade import BaseUpgrade


class Marketing(BaseUpgrade):

    def __init__(self):
        super().__init__(name="Marketing", base_cost=180.0, max_level=5)

    def get_effect_description(self) -> str:
        return f"Więcej klientów: +{(self.get_bonus() - 1) * 100:.0f}%"

    def get_bonus(self) -> float:
        return 1.0 + (self._level - 1) * 0.25

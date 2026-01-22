from .base_upgrade import BaseUpgrade


class TablesUpgrade(BaseUpgrade):

    def __init__(self):
        super().__init__(name="Stoliki", base_cost=250.0, max_level=5)

    def get_effect_description(self) -> str:
        return f"Pojemność pizzerii: {self.get_tables_count()} stolików"

    def get_bonus(self) -> float:
        return float(self.get_tables_count())

    def get_tables_count(self) -> int:
        return 5 + (self._level - 1) * 3

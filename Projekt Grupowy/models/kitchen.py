from abc import ABC, abstractmethod


class KitchenElement(ABC):

    def __init__(self, name: str, level: int = 1):
        self._name = name
        self._level = level

    @property
    def name(self) -> str:
        return self._name

    @property
    def level(self) -> int:
        return self._level

    @level.setter
    def level(self, value: int) -> None:
        self._level = value

    @abstractmethod
    def get_modifier(self) -> float:
        pass


class Chef(KitchenElement):

    def __init__(self, name: str = "Marco", level: int = 1):
        super().__init__(name, level)

    def get_modifier(self) -> float:
        return 1.0 / (1.0 + (self._level - 1) * 0.15)

    def get_mistake_chance(self) -> float:
        return max(0.02, 0.25 - (self._level - 1) * 0.05)

    def __str__(self) -> str:
        return f"Kucharz {self._name} (Poziom: {self._level})"


class Waiter(KitchenElement):

    def __init__(self, name: str = "Luigi", level: int = 1):
        super().__init__(name, level)

    def get_modifier(self) -> float:
        return 1.0 / (1.0 + (self._level - 1) * 0.2)

    def get_service_time(self, base_time: float = 3.0) -> float:
        return base_time * self.get_modifier()

    def __str__(self) -> str:
        return f"Kelner {self._name} (Poziom: {self._level})"


class Oven(KitchenElement):

    def __init__(self, level: int = 1):
        super().__init__("Piec", level)

    def get_modifier(self) -> float:
        return 1.0 / (1.0 + (self._level - 1) * 0.2)

    def __str__(self) -> str:
        return f"Piec (Poziom: {self._level})"


class Tables(KitchenElement):

    BASE_TABLES = 5
    TABLES_PER_LEVEL = 3

    def __init__(self, level: int = 1):
        super().__init__("Stoliki", level)

    def get_modifier(self) -> float:
        return float(self.get_count())

    def get_count(self) -> int:
        return self.BASE_TABLES + (self._level - 1) * self.TABLES_PER_LEVEL

    def __str__(self) -> str:
        return f"Stoliki (Poziom: {self._level}, Ilość: {self.get_count()})"


class Ingredients(KitchenElement):

    def __init__(self, level: int = 1):
        super().__init__("Składniki", level)

    def get_modifier(self) -> float:
        return 1.0 + (self._level - 1) * 0.1

    def get_price_bonus(self) -> float:
        return self.get_modifier()

    def __str__(self) -> str:
        return f"Jakość składników (Poziom: {self._level})"


class Marketing(KitchenElement):

    def __init__(self, level: int = 1):
        super().__init__("Marketing", level)

    def get_modifier(self) -> float:
        return 1.0 + (self._level - 1) * 0.25

    def get_customer_bonus(self) -> float:
        return self.get_modifier()

    def __str__(self) -> str:
        return f"Marketing (Poziom: {self._level})"

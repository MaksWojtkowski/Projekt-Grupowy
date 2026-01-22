from abc import abstractmethod
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interfaces import IUpgradeable


class BaseUpgrade(IUpgradeable):

    def __init__(self, name: str, base_cost: float, max_level: int = 10):
        self._name = name
        self._level = 1
        self._base_cost = base_cost
        self._max_level = max_level
        self._cost_multiplier = 1.5

    @property
    def name(self) -> str:
        return self._name

    @property
    def level(self) -> int:
        return self._level

    @property
    def max_level(self) -> int:
        return self._max_level

    def get_level(self) -> int:
        return self._level

    def get_upgrade_cost(self) -> float:
        if self._level >= self._max_level:
            return float('inf')
        return self._base_cost * (self._cost_multiplier ** (self._level - 1))

    def can_upgrade(self) -> bool:
        return self._level < self._max_level

    def upgrade(self) -> None:
        if self._level < self._max_level:
            self._level += 1

    @abstractmethod
    def get_effect_description(self) -> str:
        pass

    @abstractmethod
    def get_bonus(self) -> float:
        pass

    def __str__(self) -> str:
        if self._level >= self._max_level:
            return f"{self._name} (Poziom: {self._level}/{self._max_level}) - MAX"
        return f"{self._name} (Poziom: {self._level}/{self._max_level}) - Koszt: {self.get_upgrade_cost():.2f} zł"

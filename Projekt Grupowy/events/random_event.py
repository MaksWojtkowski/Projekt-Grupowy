from abc import ABC, abstractmethod
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class RandomEvent(ABC):

    def __init__(self, name: str, description: str, occurrence_chance: float):
        self._name = name
        self._description = description
        self._occurrence_chance = occurrence_chance
        self._is_active = False

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def occurrence_chance(self) -> float:
        return self._occurrence_chance

    @property
    def is_active(self) -> bool:
        return self._is_active

    @abstractmethod
    def trigger(self, game_engine) -> str:
        pass

    @abstractmethod
    def apply_effect(self, game_engine) -> None:
        pass

    @abstractmethod
    def remove_effect(self, game_engine) -> None:
        pass

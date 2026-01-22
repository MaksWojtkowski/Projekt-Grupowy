from abc import ABC, abstractmethod
from typing import Any
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class BaseAction(ABC):

    def __init__(self, game_engine):
        self._game_engine = game_engine

    @property
    def game_engine(self):
        return self._game_engine

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass

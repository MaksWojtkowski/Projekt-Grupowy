from abc import ABC, abstractmethod


class IPreparable(ABC):

    @abstractmethod
    def get_preparation_time(self) -> float:
        pass

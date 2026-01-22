from abc import ABC, abstractmethod


class ISellable(ABC):

    @abstractmethod
    def calculate_price(self) -> float:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

from abc import abstractmethod
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from interfaces import ISellable, IPreparable


class Pizza(ISellable, IPreparable):

    def __init__(self, name: str, base_price: float, ingredient_cost: float, preparation_time: float):
        self.__name = name
        self.__base_price = base_price
        self.__ingredient_cost = ingredient_cost
        self.__preparation_time = preparation_time

    @property
    def name(self) -> str:
        return self.__name

    @property
    def base_price(self) -> float:
        return self.__base_price

    @property
    def ingredient_cost(self) -> float:
        return self.__ingredient_cost

    @property
    def preparation_time(self) -> float:
        return self.__preparation_time

    def get_name(self) -> str:
        return self.__name

    def get_preparation_time(self) -> float:
        return self.__preparation_time

    @abstractmethod
    def calculate_price(self) -> float:
        pass

    def get_profit(self) -> float:
        return self.calculate_price() - self.__ingredient_cost

    def __str__(self) -> str:
        return f"{self.__name} - {self.calculate_price():.2f} zł"

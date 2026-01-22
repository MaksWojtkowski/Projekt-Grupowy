from typing import List
from .pizza import Pizza


class Order:

    __order_counter = 0

    def __init__(self, pizzas: List[Pizza]):
        Order.__order_counter += 1
        self.__order_id = Order.__order_counter
        self.__pizzas = pizzas
        self.__is_completed = False
        self.__total_price = sum(pizza.calculate_price() for pizza in pizzas)
        self.__preparation_time = sum(pizza.get_preparation_time() for pizza in pizzas)

    @property
    def order_id(self) -> int:
        return self.__order_id

    @property
    def pizzas(self) -> List[Pizza]:
        return self.__pizzas.copy()

    @property
    def total_price(self) -> float:
        return self.__total_price

    @property
    def preparation_time(self) -> float:
        return self.__preparation_time

    @property
    def is_completed(self) -> bool:
        return self.__is_completed

    def complete(self) -> None:
        self.__is_completed = True

    def get_profit(self) -> float:
        return sum(pizza.get_profit() for pizza in self.__pizzas)

    def __str__(self) -> str:
        pizza_names = ", ".join(p.get_name() for p in self.__pizzas)
        return f"Zamówienie #{self.__order_id}: {pizza_names} - {self.__total_price:.2f} zł"

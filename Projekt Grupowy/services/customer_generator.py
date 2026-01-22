import random
from typing import List, Callable
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import Customer, Order, Pizza, Margherita, Pepperoni, Hawaiian, Prosciutto


class CustomerGenerator:

    def __init__(self, seed: int = None):
        if seed is not None:
            random.seed(seed)
        self._pizza_classes: List[type] = [Margherita, Pepperoni, Hawaiian, Prosciutto]

    def generate_customers(self, count: int, min_patience: float = 20.0, max_patience: float = 60.0) -> List[Customer]:
        generate_single: Callable[[int], Customer] = lambda i: self._create_customer(min_patience, max_patience)
        return list(map(generate_single, range(count)))

    def _create_customer(self, min_patience: float, max_patience: float) -> Customer:
        patience = random.uniform(min_patience, max_patience)
        order = self._generate_order()
        customer = Customer(patience=patience, order=order)
        return customer

    def _generate_order(self) -> Order:
        pizza_count = random.randint(1, 3)
        pizza_selector: Callable[[], Pizza] = lambda: random.choice(self._pizza_classes)()
        pizzas = [pizza_selector() for _ in range(pizza_count)]
        return Order(pizzas)

    def set_pizza_classes(self, pizza_classes: List[type]) -> None:
        self._pizza_classes = pizza_classes

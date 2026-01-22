from .pizza import Pizza


class Pepperoni(Pizza):

    def __init__(self):
        super().__init__(
            name="Pepperoni",
            base_price=32.0,
            ingredient_cost=12.0,
            preparation_time=6.0
        )

    def calculate_price(self) -> float:
        return self.base_price * 1.1

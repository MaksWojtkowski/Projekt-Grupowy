from .pizza import Pizza


class Prosciutto(Pizza):

    def __init__(self):
        super().__init__(
            name="Prosciutto",
            base_price=38.0,
            ingredient_cost=15.0,
            preparation_time=8.0
        )

    def calculate_price(self) -> float:
        return self.base_price * 1.15

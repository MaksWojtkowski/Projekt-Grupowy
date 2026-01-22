from .pizza import Pizza


class Margherita(Pizza):

    def __init__(self):
        super().__init__(
            name="Margherita",
            base_price=24.0,
            ingredient_cost=8.0,
            preparation_time=5.0
        )

    def calculate_price(self) -> float:
        return self.base_price

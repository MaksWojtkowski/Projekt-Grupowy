from .pizza import Pizza


class Hawaiian(Pizza):

    def __init__(self):
        super().__init__(
            name="Hawaiian",
            base_price=30.0,
            ingredient_cost=11.0,
            preparation_time=7.0
        )

    def calculate_price(self) -> float:
        return self.base_price + 5.0

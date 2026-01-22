from .order import Order


class Customer:

    __name_counter = 0
    __names = ["Anna", "Jan", "Maria", "Piotr", "Katarzyna", "Tomasz", "Agnieszka", "Michał",
               "Ewa", "Krzysztof", "Małgorzata", "Andrzej", "Barbara", "Paweł", "Zofia"]

    def __init__(self, name: str = None, patience: float = 30.0, order: Order = None):
        Customer.__name_counter += 1
        if name is None:
            name = Customer.__names[Customer.__name_counter % len(Customer.__names)]
        self.__name = name
        self.__patience = patience
        self.__order = order
        self.__customer_id = Customer.__name_counter

    @property
    def customer_id(self) -> int:
        return self.__customer_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def patience(self) -> float:
        return self.__patience

    @property
    def order(self) -> Order:
        return self.__order

    @order.setter
    def order(self, value: Order) -> None:
        self.__order = value

    def is_satisfied(self, service_time: float) -> bool:
        return service_time <= self.__patience

    def get_tip(self, service_time: float) -> float:
        if service_time <= self.__patience * 0.5:
            return self.__order.total_price * 0.15
        elif service_time <= self.__patience * 0.75:
            return self.__order.total_price * 0.10
        elif service_time <= self.__patience:
            return self.__order.total_price * 0.05
        return 0.0

    def __str__(self) -> str:
        return f"Klient #{self.__customer_id}: {self.__name} (cierpliwość: {self.__patience:.0f}s)"

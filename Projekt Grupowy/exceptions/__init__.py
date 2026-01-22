class PizzeriaException(Exception):
    pass


class InsufficientFundsException(PizzeriaException):

    def __init__(self, required: float, available: float):
        self.required = required
        self.available = available
        super().__init__(f"Niewystarczające środki. Wymagane: {required:.2f} zł, dostępne: {available:.2f} zł")


class OutOfStockException(PizzeriaException):

    def __init__(self, item_name: str):
        self.item_name = item_name
        super().__init__(f"Brak w magazynie: {item_name}")


class CustomerLeftException(PizzeriaException):

    def __init__(self, customer_name: str, waited_time: float):
        self.customer_name = customer_name
        self.waited_time = waited_time
        super().__init__(f"Klient {customer_name} wyszedł po {waited_time:.1f}s oczekiwania")


class BankruptcyException(PizzeriaException):

    def __init__(self, final_balance: float):
        self.final_balance = final_balance
        super().__init__(f"Bankructwo! Końcowy bilans: {final_balance:.2f} zł")


class InvalidActionException(PizzeriaException):

    def __init__(self, action: str):
        self.action = action
        super().__init__(f"Nieprawidłowa akcja: {action}")


class RouteNotFoundException(PizzeriaException):

    def __init__(self, command: str):
        self.command = command
        super().__init__(f"Nie znaleziono komendy: {command}")


class ReflectionException(PizzeriaException):

    def __init__(self, class_name: str, reason: str = None):
        self.class_name = class_name
        message = f"Błąd refleksji dla klasy: {class_name}"
        if reason:
            message += f". Powód: {reason}"
        super().__init__(message)

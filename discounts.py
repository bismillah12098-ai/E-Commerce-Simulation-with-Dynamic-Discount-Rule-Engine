from models import Cart
from abc import ABC, abstractmethod
from typing import List

class IDiscount(ABC):
    @abstractmethod
    def apply(self, cart: Cart) -> float:
        pass
    @property
    @abstractmethod
    def description(self) -> str:
        pass

class BaseDiscount(IDiscount):
    def apply(self, cart: Cart) -> float:
        return 0.0
    @property
    def description(self) -> str:
        return "No discount"

class PercentageDiscount(BaseDiscount):
    def __init__(self, percentage: float):
        self._percentage = percentage
    def apply(self, cart: Cart) -> float:
        discount = round(cart.subtotal * (self._percentage / 100.0), 2)
        return discount
    @property
    def description(self) -> str:
        return f"{self._percentage}% off"

class FlatDiscount(BaseDiscount):
    def __init__(self, amount: float):
        self._amount = amount
    def apply(self, cart: Cart) -> float:
        return min(round(self._amount,2), cart.subtotal)
    @property
    def description(self) -> str:
        return f"Flat {self._amount} off"

from models import Cart, CartItem, Product
from typing import Optional

class CartBuilder:
    def __init__(self):
        self._cart = Cart(id=str(""))

    def start(self, cart_id: str):
        self._cart = Cart(id=cart_id, items=[])
        return self

    def add_product(self, product: Product, quantity: int = 1):
        existing = next((ci for ci in self._cart.items if ci.product.id == product.id), None)
        if existing:
            existing.quantity += quantity
        else:
            self._cart.items.append(CartItem(product=product, quantity=quantity))
        return self

    def with_tax(self, tax_amount: float):
        self._cart.tax = round(tax_amount,2)
        return self

    def build(self) -> Cart:
        return self._cart

from typing import Dict, Optional, List
from factories import ElectronicsFactory, BooksFactory, ProductFactory
from models import Product, Cart, Order
from discounts import IDiscount
from datetime import datetime
from threading import Lock

# Simple in-memory catalog service
class CatalogService:
    def __init__(self):
        self._products: Dict[str, Product] = {}
        # seed using factories
        ef = ElectronicsFactory()
        bf = BooksFactory()
        p1 = ef.create_sample_product("p-elec-1")
        p2 = bf.create_sample_product("p-book-1")
        self.add_product(p1)
        self.add_product(p2)

    def get_all(self):
        return list(self._products.values())

    def get_by_id(self, id: str) -> Optional[Product]:
        return self._products.get(id)

    def add_product(self, product: Product):
        self._products[product.id] = product

    def update_price(self, product_id: str, new_price: float):
        p = self._products.get(product_id)
        if p:
            old = p.price
            p.price = round(new_price,2)
            if new_price < p.last_known_price:
                print(f"Price drop detected for {p.name}: {old} -> {new_price}")
            p.last_known_price = round(new_price,2)

# Singleton Inventory
class InventorySingleton:
    _instance = None
    _lock = Lock()

    def __init__(self):
        self._stock: Dict[str,int] = {}

    @classmethod
    def instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = InventorySingleton()
        return cls._instance

    def set_stock(self, product_id: str, qty: int):
        self._stock[product_id] = qty

    def get_stock(self, product_id: str) -> int:
        return self._stock.get(product_id, 0)

    def try_reserve(self, product_id: str, qty: int) -> bool:
        cur = self._stock.get(product_id, 0)
        if cur >= qty:
            self._stock[product_id] = cur - qty
            return True
        else:
            return False

    def increase_stock(self, product_id: str, qty: int):
        cur = self._stock.get(product_id, 0)
        self._stock[product_id] = cur + qty

# Facade for checkout
class CheckoutFacade:
    def __init__(self, catalog: CatalogService, inventory: InventorySingleton):
        self.catalog = catalog
        self.inventory = inventory

    def checkout(self, cart: Cart, discounts: List[IDiscount], tax_rate: float = 0.0) -> Order:
        if not cart:
            raise ValueError("Cart is required")
        total_discount = 0.0
        for d in discounts or []:
            total_discount += d.apply(cart)
        cart.discount_amount = min(round(total_discount,2), cart.subtotal)
        cart.tax = round((cart.subtotal - cart.discount_amount) * tax_rate, 2)
        # reserve inventory
        for item in cart.items:
            stock = self.inventory.get_stock(item.product.id)
            if stock < item.quantity:
                raise RuntimeError(f"Insufficient stock for {item.product.name}")
            ok = self.inventory.try_reserve(item.product.id, item.quantity)
            if not ok:
                raise RuntimeError(f"Failed to reserve stock for {item.product.name}")
        order = Order(id=str(datetime.utcnow().timestamp()).replace('.',''), cart=cart, created_at=datetime.utcnow(), status="Paid")
        print(f"Order {order.id} created, total: {cart.total}")
        return order

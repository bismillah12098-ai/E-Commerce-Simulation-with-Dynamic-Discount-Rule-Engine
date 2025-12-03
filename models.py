from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Product(BaseModel):
    id: str
    name: str
    category_id: str
    price: float
    description: Optional[str] = ""
    last_known_price: float

class Category(BaseModel):
    id: str
    name: str

class CartItem(BaseModel):
    product: Product
    quantity: int

class Cart(BaseModel):
    id: str
    items: List[CartItem] = []
    discount_amount: float = 0.0
    tax: float = 0.0

    @property
    def subtotal(self) -> float:
        return round(sum(item.product.price * item.quantity for item in self.items), 2)

    @property
    def total(self) -> float:
        return round(self.subtotal - self.discount_amount + self.tax, 2)

class Order(BaseModel):
    id: str
    cart: Cart
    created_at: datetime
    status: str = "Created"

# Request models for endpoints
class BuildCartItemReq(BaseModel):
    product_id: str
    quantity: int

class BuildCartReq(BaseModel):
    items: List[BuildCartItemReq]
    tax: float = 0.0

class ApplyDiscountsReq(BaseModel):
    cart: Cart
    percent_discount: Optional[float] = None
    flat_discount: Optional[float] = None
    tax: float = 0.0

class CheckoutReq(BaseModel):
    cart: Cart
    percent_discount: Optional[float] = None
    flat_discount: Optional[float] = None
    tax_rate: float = 0.0

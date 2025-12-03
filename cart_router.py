from fastapi import APIRouter, Request, HTTPException
from models import BuildCartReq, ApplyDiscountsReq, Cart
from builder import CartBuilder
from discounts import PercentageDiscount, FlatDiscount

router = APIRouter()

@router.post("/build", response_model=Cart)
def build_cart(req: BuildCartReq, request: Request):
    catalog = request.app.state.catalog
    import uuid
    builder = CartBuilder().start(cart_id="cart-" + uuid.uuid4().hex)
    for item in req.items:
        p = catalog.get_by_id(item.product_id)
        if not p:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        builder.add_product(p, item.quantity)
    builder.with_tax(req.tax)
    return builder.build()

@router.post("/apply-discounts", response_model=Cart)
def apply_discounts(req: ApplyDiscountsReq, request: Request):
    cart = req.cart
    discounts = []
    if req.percent_discount is not None:
        discounts.append(PercentageDiscount(req.percent_discount))
    if req.flat_discount is not None:
        discounts.append(FlatDiscount(req.flat_discount))
    total_discount = sum(d.apply(cart) for d in discounts)
    cart.discount_amount = min(round(total_discount,2), cart.subtotal)
    cart.tax = round(req.tax,2)
    return cart

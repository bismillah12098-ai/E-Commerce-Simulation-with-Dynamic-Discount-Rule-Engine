from fastapi import APIRouter, Request, HTTPException
from models import CheckoutReq, Order
from services import CheckoutFacade
from discounts import PercentageDiscount, FlatDiscount

router = APIRouter()

@router.post("/checkout", response_model=Order)
def checkout(req: CheckoutReq, request: Request):
    catalog = request.app.state.catalog
    inventory = request.app.state.inventory
    facade = CheckoutFacade(catalog, inventory)
    discounts = []
    if req.percent_discount is not None:
        discounts.append(PercentageDiscount(req.percent_discount))
    if req.flat_discount is not None:
        discounts.append(FlatDiscount(req.flat_discount))
    try:
        order = facade.checkout(req.cart, discounts, req.tax_rate)
        return order
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

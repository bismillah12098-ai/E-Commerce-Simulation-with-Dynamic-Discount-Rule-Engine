from fastapi import APIRouter, Request, Body, HTTPException
from models import Product
from factories import ElectronicsFactory
from typing import List

router = APIRouter()

@router.get("/", response_model=List[Product])
def list_products(request: Request):
    catalog = request.app.state.catalog
    return catalog.get_all()

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: str, request: Request):
    catalog = request.app.state.catalog
    p = catalog.get_by_id(product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p

@router.post("/seed", response_model=Product)
def seed_product(request: Request):
    catalog = request.app.state.catalog
    ef = ElectronicsFactory()
    newp = ef.create_sample_product("p-elec-2")
    catalog.add_product(newp)
    return newp

@router.post("/{product_id}/price")
def update_price(product_id: str, new_price: float = Body(..., embed=True), request: Request = None):
    catalog = request.app.state.catalog
    p = catalog.get_by_id(product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    catalog.update_price(product_id, new_price)
    return {"status":"ok", "product_id": product_id}

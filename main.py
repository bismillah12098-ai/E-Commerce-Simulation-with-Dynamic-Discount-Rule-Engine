from fastapi import APIRouter, Request, HTTPException
from typing import List, Dict, Any
from pydantic import BaseModel

# --- Response Models ---

class ProductResponse(BaseModel):
    product_id: str
    name: str
    category: str
    price: float
    stock: int
    description: str

class AllProductsResponse(BaseModel):
    products: List[ProductResponse]

# --- Router Setup ---

router = APIRouter()

# --- Utility Function to get Services from App State ---

def get_services(request: Request) -> Dict[str, Any]:
    """Helper to retrieve services attached to the app state."""
    return {
        "catalog": request.app.state.catalog,
        "inventory": request.app.state.inventory,
    }

# --- Routes ---

@router.get("/", response_model=AllProductsResponse, summary="List all products with current stock")
def list_products(request: Request):
    """Retrieves a list of all products in the catalog along with their current stock levels."""
    services = get_services(request)
    catalog = services["catalog"]
    inventory = services["inventory"]

    products_data = []
    for product in catalog.get_all_products():
        stock = inventory.get_stock(product.product_id)
        products_data.append(ProductResponse(
            **product.__dict__,
            stock=stock
        ))
    
    return {"products": products_data}


@router.get("/{product_id}", response_model=ProductResponse, summary="Get product details and stock")
def get_product(product_id: str, request: Request):
    """Retrieves detailed information and stock for a specific product."""
    services = get_services(request)
    catalog = services["catalog"]
    inventory = services["inventory"]

    product = catalog.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product '{product_id}' not found.")
    
    stock = inventory.get_stock(product_id)

    return ProductResponse(
        **product.__dict__,
        stock=stock
    )
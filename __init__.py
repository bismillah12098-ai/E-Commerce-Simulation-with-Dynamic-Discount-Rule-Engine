# make routers package
from .products_router import router as products_router
from .cart_router import router as cart_router
from .orders_router import router as orders_router

# export names matching what main imports
products_router = products_router
cart_router = cart_router
orders_router = orders_router

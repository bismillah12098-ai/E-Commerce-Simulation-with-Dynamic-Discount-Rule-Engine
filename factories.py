from models import Product, Category
from uuid import uuid4

# Factory Method for Product
class ProductFactory:
    @staticmethod
    def create_product(id: str, name: str, category_id: str, price: float, description: str = "") -> Product:
        return Product(id=id, name=name, category_id=category_id, price=round(price,2), description=description, last_known_price=round(price,2))

# Abstract Factory for categories + sample product
class ICategoryFactory:
    def create_category(self, id: str, name: str) -> Category:
        raise NotImplementedError()
    def create_sample_product(self, product_id: str) -> Product:
        raise NotImplementedError()

class ElectronicsFactory(ICategoryFactory):
    def create_category(self, id: str, name: str) -> Category:
        return Category(id=id, name=name)
    def create_sample_product(self, product_id: str) -> Product:
        return ProductFactory.create_product(product_id, "Wireless Headphones", "electronics", 79.99, "Bluetooth headphones")

class BooksFactory(ICategoryFactory):
    def create_category(self, id: str, name: str) -> Category:
        return Category(id=id, name=name)
    def create_sample_product(self, product_id: str) -> Product:
        return ProductFactory.create_product(product_id, "C# In Depth", "books", 39.99, "Programming book")

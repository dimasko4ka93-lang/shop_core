from typing import List


class Product:
    """Класс для описания товара в интернет-магазине."""

    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """Класс для описания категории товаров."""

    name: str
    description: str
    products: List[Product]

    # Атрибуты класса — общие для всех объектов
    category_count: int = 0
    product_count: int = 0

    def __init__(
        self, name: str, description: str, products: List[Product]
    ) -> None:
        self.name = name
        self.description = description
        self.products = products

        # Автоматическое заполнение атрибутов класса
        Category.category_count += 1
        Category.product_count += len(products)

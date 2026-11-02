from typing import List


class Product:
    """Класс для описания товара в интернет-магазине."""

    name: str
    description: str
    __price: float
    quantity: int

    def __init__(self, name: str, description: str, price: float, quantity: int) -> None:
        self.name = name
        self.description = description
        self.__price = price  # Теперь цена приватная
        self.quantity = quantity

    @classmethod
    def new_product(cls, product_data: dict, existing_products: list = None) -> "Product":
        """
        Класс-метод для создания товара из словаря.
        Если передан список existing_products, ищет дубликаты по имени.
        """
        if existing_products is not None:
            for existing_product in existing_products:
                if existing_product.name == product_data["name"]:
                    # Суммируем количество
                    existing_product.quantity += product_data["quantity"]
                    # Выбираем максимальную цену
                    if product_data["price"] > existing_product.price:
                        existing_product.price = product_data["price"]
                    return existing_product

        # Если дубликатов не найдено или список не передан, создаем новый товар
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"]
        )

    @property
    def price(self) -> float:
        """Геттер для цены."""
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Сеттер для цены с проверкой."""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price


class Category:
    """Класс для описания категории товаров."""

    name: str
    description: str
    __products: List[Product]

    # Атрибуты класса — общие для всех объектов
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = products  # Теперь список товаров приватный

        # Автоматическое заполнение атрибутов класса при создании категории
        Category.category_count += 1
        # product_count теперь увеличивается только через add_product,
        # но если мы передаем список при создании, логично учесть его:
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Метод для добавления продукта в категорию."""
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер для вывода списка товаров в виде строки."""
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result

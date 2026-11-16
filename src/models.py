from abc import ABC, abstractmethod


# --- Задание 2: Класс-миксин ---
class InfoMixin:
    """Миксин, который печатает информацию о созданном объекте."""

    def __init__(self, *args, **kwargs):
        # super() вызовет следующий класс в цепочке MRO (в нашем случае BaseProduct)
        super().__init__(*args, **kwargs)
        print(f"Создан объект {self.__class__.__name__}({self})")


# --- Задание 1: Базовый абстрактный класс ---
class BaseProduct(ABC):
    """Абстрактный базовый класс для всех продуктов."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        if quantity == 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self):
        """Строковое представление продукта."""
        pass

    def __add__(self, other):
        """Сложение товаров одного класса."""
        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одного класса")
        return (self.price * self.quantity) + (other.price * other.quantity)

    @classmethod
    def new_product(cls, product_data: dict, existing_products: list = None) -> "BaseProduct":
        """Класс-метод для создания товара из словаря."""
        if existing_products is not None:
            for existing_product in existing_products:
                if existing_product.name == product_data["name"]:
                    existing_product.quantity += product_data["quantity"]
                    if product_data["price"] > existing_product.price:
                        existing_product.price = product_data["price"]
                    return existing_product

        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"]
        )

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price


# --- Класс Product: теперь наследуется от BaseProduct и InfoMixin ---
class Product(InfoMixin, BaseProduct):
    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self):
        return self.__str__()


# --- Классы-наследники ---
class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __str__(self):
        return super().__str__()  # используем строку из Product


class LawnGrass(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __str__(self):
        return super().__str__()


class Category:
    product_count = 0
    category_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products
        Category.category_count += 1

    @property
    def products(self) -> list:
        # В файле main.py выводится len(category1.products) и печать списка.
        # Поэтому здесь лучше возвращать список, а не строку.
        return self.__products

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product: BaseProduct) -> None:
        if not isinstance(product, BaseProduct):
            raise TypeError("В категорию можно добавлять только объекты класса Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    def middle_price(self) -> float:
        """Подсчёт средней цены товаров в категории."""
        try:
            total = sum(product.price for product in self.__products)
            return total / len(self.__products)
        except ZeroDivisionError:
            return 0

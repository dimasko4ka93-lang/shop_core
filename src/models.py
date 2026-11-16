class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    # Задание 2: складываем только объекты строго одного класса
    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одного класса")
        return (self.price * self.quantity) + (other.price * other.quantity)

    @classmethod
    def new_product(cls, product_data: dict, existing_products: list = None) -> "Product":
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


class Smartphone(Product):
    """Смартфон — наследник Product."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: float, model: str, memory: int, color: str):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Трава газонная — наследник Product."""

    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: str, color: str):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    product_count = 0

    def __init__(self, name: str, description: str, products: list):
        self.name = name
        self.description = description
        self.__products = products

    @property
    def products(self) -> str:
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    # Задание 3: добавляем только Product или его наследников
    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError(
                "В категорию можно добавлять только объекты класса Product или его наследников"
            )
        self.__products.append(product)
        Category.product_count += 1

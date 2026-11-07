import pytest

from src.models import Category, Product


@pytest.fixture
def product():
    return Product("Test Product", "Test Description", 100.0, 5)


@pytest.fixture
def category(product):
    return Category("Test Category", "Test Category Description", [product])


def test_add_product_increases_count(category, product):
    """Тест: метод add_product добавляет товар и увеличивает счетчик."""
    initial_count = Category.product_count
    new_product = Product("New Product", "Desc", 200.0, 2)
    category.add_product(new_product)

    assert Category.product_count == initial_count + 1
    # Проверяем, что товар действительно добавился в список (через геттер)
    assert "New Product" in category.products


def test_products_getter_format(category):
    """Тест: геттер products возвращает строку в правильном формате."""
    expected = "Test Product, 100.0 руб. Остаток: 5 шт.\n"
    assert category.products == expected


def test_new_product_creates_instance():
    """Тест: класс-метод new_product создает экземпляр Product."""
    data = {"name": "New", "description": "Desc", "price": 50.0, "quantity": 10}
    p = Product.new_product(data)

    assert isinstance(p, Product)
    assert p.name == "New"
    assert p.price == 50.0
    assert p.quantity == 10

    def test_product_str(product):
        """Тест: строковое представление продукта."""
        assert str(product) == "Test Product, 100.0 руб. Остаток: 5 шт."

    def test_category_str(category):
        """Тест: строковое представление категории."""
        assert str(category) == "Test Category, количество продуктов: 5 шт."

    def test_product_add():
        """Тест: сложение двух продуктов = сумма произведений цены на количество."""
        p1 = Product("A", "Desc", 100.0, 10)
        p2 = Product("B", "Desc", 200.0, 2)
        assert (p1 + p2) == 1400

    def test_product_add_type_error():
        """Тест: сложение с не-Product вызывает TypeError."""
        p1 = Product("A", "Desc", 100.0, 10)
        with pytest.raises(TypeError):
            p1 + 10


def test_price_setter_positive(product):
    """Тест: сеттер устанавливает положительную цену."""
    product.price = 200.0
    assert product.price == 200.0


def test_price_setter_negative_and_zero(product, capsys):
    """Тест: сеттер не устанавливает отрицательную или нулевую цену и выводит сообщение."""
    # Изначальная цена 100.0
    product.price = -50
    assert product.price == 100.0  # Цена не изменилась

    product.price = 0
    assert product.price == 100.0  # Цена не изменилась

    # Проверяем, что сообщение вывелось 2 раза (для -50 и для 0)
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_new_product_with_duplicates():
    """Тест: new_product обновляет существующий товар, суммирует количество и берет макс. цену."""
    # 1. Создаем существующий товар
    existing_product = Product("Samsung", "Desc", 100.0, 5)

    # 2. Готовим данные для "нового" товара с таким же именем, большей ценой и другим количеством
    product_data = {"name": "Samsung", "description": "Desc", "price": 150.0, "quantity": 10}

    # 3. Вызываем new_product, передавая список существующих товаров
    result_product = Product.new_product(product_data, existing_products=[existing_product])

    # 4. Проверяем, что вернулся тот же самый объект (не создался новый)
    assert result_product is existing_product

    # 5. Проверяем, что количество сложилось (5 + 10 = 15)
    assert result_product.quantity == 15

    # 6. Проверяем, что цена обновилась на максимальную (150.0 > 100.0)
    assert result_product.price == 150.0

import pytest

from src.models import Category, LawnGrass, Product, Smartphone


@pytest.fixture
def product():
    return Product("Test Product", "Test Description", 100.0, 5)


@pytest.fixture
def category(product):
    return Category("Test Category", "Test Category Description", [product])


@pytest.fixture
def smartphone():
    return Smartphone(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера",
        180000.0, 5, 95.5, "S23 Ultra", 256, "Серый"
    )


@pytest.fixture
def lawn_grass():
    return LawnGrass(
        "Газонная трава", "Элитная трава для газона",
        500.0, 20, "Россия", "7 дней", "Зеленый"
    )


# ---------- Базовые тесты ----------

def test_add_product_increases_count(category):
    initial_count = Category.product_count
    new_product = Product("New Product", "Desc", 200.0, 2)
    category.add_product(new_product)

    assert Category.product_count == initial_count + 1
    # Проверяем, что товар в списке по имени
    assert any(p.name == "New Product" for p in category.products)


def test_products_getter_format(category):
    # Геттер теперь возвращает список объектов, а не строку
    assert isinstance(category.products, list)
    assert len(category.products) == 1
    assert category.products[0].name == "Test Product"
    assert category.products[0].price == 100.0
    assert category.products[0].quantity == 5


def test_new_product_creates_instance():
    data = {"name": "New", "description": "Desc", "price": 50.0, "quantity": 10}
    p = Product.new_product(data)

    assert isinstance(p, Product)
    assert p.name == "New"
    assert p.price == 50.0
    assert p.quantity == 10


def test_product_str(product):
    assert str(product) == "Test Product, 100.0 руб. Остаток: 5 шт."


def test_category_str(category):
    assert str(category) == "Test Category, количество продуктов: 5 шт."


def test_product_add():
    p1 = Product("A", "Desc", 100.0, 10)
    p2 = Product("B", "Desc", 200.0, 2)
    assert (p1 + p2) == 1400


def test_product_add_type_error():
    p1 = Product("A", "Desc", 100.0, 10)
    with pytest.raises(TypeError):
        p1 + 10


def test_price_setter_positive(product):
    product.price = 200.0
    assert product.price == 200.0


def test_price_setter_negative_and_zero(product, capsys):
    product.price = -50
    assert product.price == 100.0

    product.price = 0
    assert product.price == 100.0

    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out


def test_new_product_with_duplicates():
    existing_product = Product("Samsung", "Desc", 100.0, 5)
    product_data = {"name": "Samsung", "description": "Desc", "price": 150.0, "quantity": 10}

    result_product = Product.new_product(product_data, existing_products=[existing_product])

    assert result_product is existing_product
    assert result_product.quantity == 15
    assert result_product.price == 150.0


def test_smartphone_creation(smartphone):
    assert smartphone.name == "Samsung Galaxy S23 Ultra"
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "S23 Ultra"
    assert smartphone.memory == 256
    assert smartphone.color == "Серый"


def test_lawn_grass_creation(lawn_grass):
    assert lawn_grass.name == "Газонная трава"
    assert lawn_grass.country == "Россия"
    assert lawn_grass.germination_period == "7 дней"
    assert lawn_grass.color == "Зеленый"


def test_smartphone_is_product(smartphone):
    assert isinstance(smartphone, Product)


def test_lawn_grass_is_product(lawn_grass):
    assert isinstance(lawn_grass, Product)


def test_add_same_type_smartphones():
    s1 = Smartphone("Samsung", "Desc", 1000.0, 2, 95.5, "S23", 256, "Black")
    s2 = Smartphone("Iphone", "Desc", 2000.0, 3, 98.2, "15", 512, "Gray")
    assert (s1 + s2) == 8000  # 1000*2 + 2000*3


def test_add_same_type_lawn_grass():
    g1 = LawnGrass("Grass1", "Desc", 500.0, 2, "Россия", "7 дней", "Зеленый")
    g2 = LawnGrass("Grass2", "Desc", 450.0, 3, "США", "5 дней", "Темно-зеленый")
    assert (g1 + g2) == 2350  # 500*2 + 450*3


def test_add_different_types_raises(smartphone, lawn_grass):
    with pytest.raises(TypeError):
        smartphone + lawn_grass


def test_add_product_and_smartphone_raises(product, smartphone):
    with pytest.raises(TypeError):
        product + smartphone


def test_add_product_valid(category, smartphone):
    category.add_product(smartphone)
    # Проверяем, что смартфон есть в списке по имени
    assert any(p.name == "Samsung Galaxy S23 Ultra" for p in category.products)


def test_add_product_invalid_raises(category):
    with pytest.raises(TypeError):
        category.add_product("Not a product")


def test_add_product_invalid_int_raises(category):
    with pytest.raises(TypeError):
        category.add_product(42)


def test_mixin_prints_info(capsys):
    """Тест: миксин печатает информацию о создании объекта."""
    product = Product("Test", "Desc", 100.0, 5)
    captured = capsys.readouterr()
    assert "Создан объект Product(" in captured.out
    assert product.name == "Test"  # ← добавили использование


def test_product_zero_quantity_raises():
    """Тест: создание Product с quantity=0 вызывает ValueError."""
    with pytest.raises(ValueError, match="Товар с нулевым количеством не может быть добавлен"):
        Product("Test", "Desc", 100.0, 0)


def test_middle_price_with_products():
    """Тест: middle_price возвращает среднюю цену."""
    p1 = Product("A", "Desc", 100.0, 1)
    p2 = Product("B", "Desc", 200.0, 2)
    category = Category("Test", "Desc", [p1, p2])
    assert category.middle_price() == 150.0


def test_middle_price_empty_category():
    """Тест: middle_price для пустой категории возвращает 0."""
    category = Category("Empty", "Desc", [])
    assert category.middle_price() == 0

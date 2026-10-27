import os

import pytest

from src.models import Category, Product
from src.utils import load_categories_from_json


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сбрасываем счётчики класса перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def sample_products():
    return [
        Product("Samsung Galaxy S23 Ultra", "256GB", 180000.0, 5),
        Product("Iphone 15", "512GB", 210000.0, 8),
    ]


def test_product_init():
    """Корректная инициализация объекта Product."""
    product = Product("Iphone 15", "512GB", 210000.0, 8)
    assert product.name == "Iphone 15"
    assert product.description == "512GB"
    assert product.price == 210000.0
    assert product.quantity == 8


def test_category_init(sample_products):
    """Корректная инициализация объекта Category."""
    category = Category("Смартфоны", "Описание", sample_products)
    assert category.name == "Смартфоны"
    assert category.description == "Описание"
    assert category.products == sample_products
    assert len(category.products) == 2


def test_category_count(sample_products):
    """Подсчёт количества категорий."""
    assert Category.category_count == 0
    Category("Смартфоны", "Описание", sample_products)
    assert Category.category_count == 1
    Category("Телевизоры", "Описание", [])
    assert Category.category_count == 2


def test_product_count(sample_products):
    """Подсчёт количества продуктов."""
    assert Category.product_count == 0
    Category("Смартфоны", "Описание", sample_products)
    assert Category.product_count == 2
    Category("Телевизоры", "Описание", [Product("TV", "4K", 100000.0, 3)])
    assert Category.product_count == 3


def test_load_categories_from_json():
    """Тест загрузки категорий и товаров из JSON."""
    # Формируем путь к тестовому json-файлу в той же папке
    json_path = os.path.join(os.path.dirname(__file__), "test_products.json")

    # Загружаем данные
    categories = load_categories_from_json(json_path)

    # Проверяем, что всё работает правильно
    assert len(categories) == 2
    assert categories[0].name == "Смартфоны"
    assert len(categories[0].products) == 2
    assert categories[0].products[0].name == "Iphone 15"

    # Проверяем, что счетчики класса обновились автоматически
    assert Category.category_count == 2
    assert Category.product_count == 2

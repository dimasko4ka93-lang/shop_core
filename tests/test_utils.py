import json

from src.models import Category, Product
from src.utils import load_categories_from_json


def test_load_categories_from_json(tmp_path):
    """Тест: загрузка категорий и продуктов из JSON-файла."""
    # Создаем временный JSON-файл
    test_data = [
        {
            "name": "Смартфоны",
            "description": "Описание смартфонов",
            "products": [
                {"name": "Iphone 15", "description": "512GB", "price": "210000.0", "quantity": "8"}
            ]
        }
    ]

    # tmp_path - это встроенная фикстура pytest, которая создает временную папку
    file_path = tmp_path / "test_data.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f)

    # Запускаем нашу функцию
    categories = load_categories_from_json(str(file_path))

    # Проверяем результат
    assert len(categories) == 1
    assert isinstance(categories[0], Category)
    assert categories[0].name == "Смартфоны"

    # Проверяем, что продукты создались правильно (включая приведение типов float и int)
    assert len(categories[0]._Category__products) == 1  # обращаемся к приватному атрибуту для проверки
    product = categories[0]._Category__products[0]
    assert isinstance(product, Product)
    assert product.name == "Iphone 15"
    assert product.price == 210000.0
    assert product.quantity == 8

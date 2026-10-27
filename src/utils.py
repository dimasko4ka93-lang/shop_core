import json
from typing import List

from src.models import Category, Product


def load_categories_from_json(path: str) -> List[Category]:
    """Читает JSON и возвращает список объектов Category с Product внутри."""
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    categories: List[Category] = []
    for cat in data:
        products = [
            Product(
                name=p["name"],
                description=p["description"],
                price=float(p["price"]),
                quantity=int(p["quantity"]),
            )
            for p in cat.get("products", [])
        ]
        categories.append(
            Category(
                name=cat["name"],
                description=cat["description"],
                products=products,
            )
        )
    return categories

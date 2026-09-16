import datetime
from typing import Optional, TypedDict

class User(TypedDict):
    name: str
    registered_years: int
    is_vip: bool

class Item(TypedDict):
    id: int
    price: int
    category: str
    qty: int


# Имитация базы данных в памяти
USERS_DB: dict[int, User] = {
    1: {"name": "Иван", "registered_years": 3, "is_vip": True},
    2: {"name": "Ольга", "registered_years": 1, "is_vip": False},
    3: {"name": "Иван", "registered_years": 2, "is_vip": True},
    4: {"name": "Ольга", "registered_years": 2, "is_vip": False},
    5: {"name": "Иван", "registered_years": 3, "is_vip": True},
    6: {"name": "Ольга", "registered_years": 3, "is_vip": False},
    7: {"name": "Иван", "registered_years": 4, "is_vip": True},
    8: {"name": "Ольга", "registered_years": 4, "is_vip": False},
}


def calculate_order_total(user_id: int, items: list[Item], discount_code: Optional[str] = None) -> float:
    """
    items: список словарей [{"id": 1, "price": 100,
    "category": "electronics", "qty": 2}]
    """
    user: User | None = USERS_DB.get(user_id)
    if not user:
        raise ValueError("User not found")

    total: float = 0

    item:  Item
    for item in items:
        # Считаем базовую стоимость товара
        item_total: float = item["price"] * item["qty"]

        # Легаси-правило 1:
        # скидка на электронику 5%, если куплено больше 1 штуки
        if item["category"] == "electronics" and item["qty"] > 1:
            item_total = item_total * 0.95

        # Легаси-правило 2: скидка на книги 10% всегда
        if item["category"] == "books":
            item_total = item_total * 0.90

        total += item_total

    # Применение скидок пользователя
    if user["is_vip"]:
        total -= total * 0.10  # VIP скидка 10%
    elif user["registered_years"] >= 3:
        total -= total * 0.05  # Скидка за лояльность 5%

    # Старая кривая логика промокодов
    if discount_code == "NEWYEAR2025":
        # Промокод работает только в декабре и январе (захардкожено)
        now: datetime.datetime = datetime.datetime.now()
        if now.month == 12 or now.month == 1:
            total -= 500  # Скидка 500 рублей
    elif discount_code == "SUMMER":
        total = total * 0.85  # Скидка 15%

    if total < 0:
        total = 0

    return total

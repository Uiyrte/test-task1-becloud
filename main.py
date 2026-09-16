import datetime
from typing import Optional, TypedDict
from abc import ABC, abstractmethod


class User(TypedDict):
    name: str
    registered_years: int
    is_vip: bool


class Item(TypedDict):
    id: int
    price: int
    category: str
    qty: int


class CategoryItemSale(ABC):
    @abstractmethod
    def calculate_item_cost(self, item: Item) -> float:
        pass


class ElectronicsItemSale(CategoryItemSale):
    def calculate_item_cost(self, item: Item) -> float:
        if item["qty"] > 1:
            return item["price"] * item["qty"] * 0.95
        return item["price"] * item["qty"]


class BooksItemSale(CategoryItemSale):
    def calculate_item_cost(self, item: Item) -> float:
        return item["price"] * item["qty"] * 0.9


class DefaultItemSale(CategoryItemSale):
    def calculate_item_cost(self, item: Item) -> float:
        return item["price"] * item["qty"]


ITEM_SALE_REGISTRY: dict[str, CategoryItemSale] = {
    "electronics": ElectronicsItemSale(),
    "books": BooksItemSale(),
}
DEFAULT_ITEM_SALE: CategoryItemSale = DefaultItemSale()


def get_item_sale_strategy(category: str) -> CategoryItemSale:
    return ITEM_SALE_REGISTRY.get(category, DEFAULT_ITEM_SALE)


class PersonSale(ABC):
    @abstractmethod
    def is_available(self, user: User) -> bool:
        pass

    @abstractmethod
    def calculate_total_cost(self, total: float) -> float:
        pass


class VipPersonSale(PersonSale):
    def is_available(self, user: User) -> bool:
        if user["is_vip"]:
            return True
        return False

    def calculate_total_cost(self, total: float) -> float:
        return total * 0.9


class LoyalPersonSale(PersonSale):
    def is_available(self, user: User) -> bool:
        if user["registered_years"] >= 3:
            return True
        return False

    def calculate_total_cost(self, total: float) -> float:
        return total * 0.95


PERSON_SALE_REGISTRY: list[PersonSale] = [VipPersonSale(), LoyalPersonSale()]


class DiscountCodeSale(ABC):
    @abstractmethod
    def calculate_total_cost(self, total: float) -> float:
        pass


class NewYearCodeSale(DiscountCodeSale):
    def calculate_total_cost(self, total: float) -> float:
        now: datetime.datetime = datetime.datetime.now()
        if now.month == 12 or now.month == 1:
            total -= 500
        return total


class SummerCodeSale(DiscountCodeSale):
    def calculate_total_cost(self, total: float) -> float:
        total = total * 0.85  # Скидка 15%
        return total


CODE_SALE_REGISTRY: dict[str, DiscountCodeSale] = {
    "NEWYEAR2025": NewYearCodeSale(),
    "SUMMER": SummerCodeSale(),
}

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


def calculate_order_total(
    user_id: int, items: list[Item], discount_code: Optional[str] = None
) -> float:
    """
    items: список словарей [{"id": 1, "price": 100,
    "category": "electronics", "qty": 2}]
    """
    user: User | None = USERS_DB.get(user_id)
    if not user:
        raise ValueError("User not found")

    total: float = 0

    item: Item
    for item in items:
        # Применение скидок, соответствующих категории, количетсву и т.п.
        item_sale_strategy: CategoryItemSale = get_item_sale_strategy(
            item["category"]
        )
        total += item_sale_strategy.calculate_item_cost(item)

    # Применение скидок пользователя
    for person_sale in PERSON_SALE_REGISTRY:
        if person_sale.is_available(user):
            total = person_sale.calculate_total_cost(total)
            break

    # Применение скидок промокодов
    if discount_code and discount_code in CODE_SALE_REGISTRY:
        total = CODE_SALE_REGISTRY[discount_code].calculate_total_cost(total)

    if total < 0:
        total = 0

    return total

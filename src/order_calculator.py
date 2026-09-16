from typing import Optional

from src.code_sale import CODE_SALE_REGISTRY
from src.item_sale import CategoryItemSale, get_item_sale_strategy
from src.models import Item, User
from src.person_sale import PERSON_SALE_REGISTRY
from src.users_repository import get_user_from_db


def calculate_order_total(
    user_id: int, items: list[Item], discount_code: Optional[str] = None
) -> float:
    """
    items: список словарей [{"id": 1, "price": 100,
    "category": "electronics", "qty": 2}]
    """
    user: User = get_user_from_db(user_id)

    total: float = 0

    item: Item
    for item in items:
        # Применение скидок, соответствующих категории, количетсву и т.п.
        item_sale_strategy: CategoryItemSale = get_item_sale_strategy(
            item.category
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

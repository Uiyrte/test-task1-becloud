from src.code_sale import DiscountCodeSale, apply_code_sales, get_code_sales
from src.delivery import calculate_delivery_cost
from src.item_sale import CategoryItemSale, get_item_sale_strategy
from src.models import Item, User
from src.person_sale import PERSON_SALE_REGISTRY
from src.users_repository import get_user_from_db


def calculate_order_total(
    user_id: int, items: list[Item], *discount_codes: str
) -> float:
    """
    items: список словарей [{"id": 1, "price": 100,
    "category": "electronics", "qty": 2}]
    """
    user: User = get_user_from_db(user_id)

    total: float = 0

    item: Item
    for item in items:
        # Применение скидок, соответствующих категории, количеству и т.п.
        item_sale_strategy: CategoryItemSale = get_item_sale_strategy(
            item.category
        )
        total += item_sale_strategy.calculate_item_cost(item)

    has_goods: bool = any(item.qty > 0 for item in items)

    # Применение скидок пользователя
    for person_sale in PERSON_SALE_REGISTRY:
        if person_sale.is_available(user):
            total = person_sale.calculate_total_cost(total)
            break

    # Применение скидок промокодов
    sale_codes: list[DiscountCodeSale] = get_code_sales(list(discount_codes))
    total = apply_code_sales(total, sale_codes, user, items)

    if has_goods:
        total += calculate_delivery_cost(total, sale_codes, user, items)

    return total

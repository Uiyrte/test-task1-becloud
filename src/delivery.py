from src.code_sale import DiscountCodeSale
from src.models import Item, User

BASE_DELIVERY_COST: float = 300


def calculate_delivery_cost(
    total: float,
    sale_codes: list[DiscountCodeSale],
    user: User,
    items: list[Item],
) -> float:
    delivery_cost: float = BASE_DELIVERY_COST
    for code in sale_codes:
        delivery_cost = code.calculate_delivery_cost(
            delivery_cost, total, user, items
        )

    return max(delivery_cost, 0)

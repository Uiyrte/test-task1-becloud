import datetime
from abc import ABC, abstractmethod

from src.models import Item


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
import datetime
from abc import ABC, abstractmethod
from enum import IntEnum

from src.models import Item, User


class CodeTypes(IntEnum):
    Fixed = 0
    Percent = 1
    Delivery = 2


class DiscountCodeSale(ABC):
    @property
    @abstractmethod
    def get_code_type(self) -> CodeTypes:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass

    @abstractmethod
    def calculate_total_cost(
        self, total: float, user: User, items: list[Item]
    ) -> float:
        pass


class FixedCodeSale(DiscountCodeSale):
    def __init__(self, amount: float):
        self.amount = amount

    @property
    def get_code_type(self) -> CodeTypes:
        return CodeTypes.Fixed

    def is_available(self) -> bool:
        return True

    def calculate_total_cost(
        self, total: float, user: User, items: list[Item]
    ) -> float:
        return total - self.amount


class PercentCodeSale(DiscountCodeSale):
    def __init__(self, percent: int):
        self.percent = percent

    @property
    def get_code_type(self) -> CodeTypes:
        return CodeTypes.Percent

    def is_available(self) -> bool:
        return True

    def calculate_total_cost(
        self, total: float, user: User, items: list[Item]
    ) -> float:
        if self.is_available():
            return total * (1 - self.percent / 100)
        return total


class DeliveryCodeSale(DiscountCodeSale):
    def __init__(self, limit: float, del_cost: float):
        self.limit = limit
        self.del_cost = del_cost

    @property
    def get_code_type(self) -> CodeTypes:
        return CodeTypes.Delivery

    def is_available(self) -> bool:
        return True

    def calculate_total_cost(
        self, total: float, user: User, items: list[Item]
    ) -> float:
        if total <= self.limit:
            return total + self.del_cost
        return total


class NewYearCodeDecorator(DiscountCodeSale):
    def __init__(self, wrapped: DiscountCodeSale, allowed_month: set[int]):
        self.wrapped = wrapped
        self.allowed_month = allowed_month

    @property
    def get_code_type(self) -> CodeTypes:
        return self.wrapped.get_code_type

    def is_available(self) -> bool:
        now: datetime.datetime = datetime.datetime.now()
        return now.month in self.allowed_month and self.wrapped.is_available()

    def calculate_total_cost(
        self, total: float, user: User, items: list[Item]
    ) -> float:
        if self.is_available():
            return self.wrapped.calculate_total_cost(total, user, items)
        return total


CODE_SALE_REGISTRY: dict[str, DiscountCodeSale] = {
    "NEWYEAR2025": NewYearCodeDecorator(FixedCodeSale(500), {12, 1}),
    "SUMMER": PercentCodeSale(15),
    "FREEDELIVERY": DeliveryCodeSale(limit=2000, del_cost=300),
}


def apply_code_sales(
    total: float, codes: list[str], user: User, items: list[Item]
) -> float:
    sale_codes: list[DiscountCodeSale] = [
        CODE_SALE_REGISTRY[code]
        for code in codes
        if code in CODE_SALE_REGISTRY
    ]
    sorted_codes = sorted(sale_codes, key=lambda p: p.get_code_type)

    for code in sorted_codes:
        total = code.calculate_total_cost(total, user, items)

    return max(total, 0)

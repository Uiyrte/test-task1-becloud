from abc import ABC, abstractmethod

from src.models import Item, User


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

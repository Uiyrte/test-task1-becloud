from abc import ABC, abstractmethod

from src.models import Item


class CategoryItemSale(ABC):
    @abstractmethod
    def calculate_item_cost(self, item: Item) -> float:
        pass


class ElectronicsItemSale(CategoryItemSale):
    def calculate_item_cost(self, item: Item) -> float:
        if item.qty > 1:
            return item.price * item.qty * 0.95
        return item.price * item.qty


class BooksItemSale(CategoryItemSale):
    def calculate_item_cost(self, item: Item) -> float:
        return item.price * item.qty * 0.9


class DefaultItemSale(CategoryItemSale):
    def calculate_item_cost(self, item: Item) -> float:
        return item.price * item.qty


ITEM_SALE_REGISTRY: dict[str, CategoryItemSale] = {
    "electronics": ElectronicsItemSale(),
    "books": BooksItemSale(),
}
DEFAULT_ITEM_SALE: CategoryItemSale = DefaultItemSale()


def get_item_sale_strategy(category: str) -> CategoryItemSale:
    return ITEM_SALE_REGISTRY.get(category, DEFAULT_ITEM_SALE)

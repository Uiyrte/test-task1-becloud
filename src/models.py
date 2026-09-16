from typing import TypedDict


class User(TypedDict):
    name: str
    registered_years: int
    is_vip: bool


class Item(TypedDict):
    id: int
    price: int
    category: str
    qty: int

from dataclasses import dataclass


@dataclass
class User:
    name: str
    registered_years: int
    is_vip: bool


@dataclass
class Item:
    id: int
    price: int
    category: str
    qty: int

from datetime import datetime

import pytest

from src.models import Item
from src.order_calculator import calculate_order_total
from src.users_repository import USERS_DB


def make_fake_date(month):
    class FakeDate(datetime):
        @classmethod
        def now(cls, tz=None):
            return cls(2026, month, 15)

    return FakeDate


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code"],
    [
        [-1, [], None],
        [-1, [Item(id=1, price=100, category="electronics", qty=2)], None],
        [-1, [], "NEWYEAR2025"],
        [
            -1,
            [Item(id=1, price=100, category="electronics", qty=2)],
            "NEWYEAR2025",
        ],
        [len(USERS_DB) + 1, [], None],
        [
            len(USERS_DB) + 1,
            [Item(id=1, price=100, category="electronics", qty=2)],
            None,
        ],
        [len(USERS_DB) + 1, [], "NEWYEAR2025"],
        [
            len(USERS_DB) + 1,
            [Item(id=1, price=100, category="electronics", qty=2)],
            "NEWYEAR2025",
        ],
        ["1", [], None],
    ],
)
def test_user_not_found(user_id, items, discount_code):
    with pytest.raises(ValueError, match="User not found"):
        calculate_order_total(user_id, items, discount_code)


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code"],
    [
        [1, [], None],
        [2, [], None],
        [1, [], "NEWYEAR2025"],
        [2, [], "NEWYEAR2025"],
    ],
)
def test_zero_items(user_id, items, discount_code):
    assert calculate_order_total(user_id, items, discount_code) == 0


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code"],
    [
        [2, [Item(id=1, price=100, category="base", qty=2)], None],
        [2, [Item(id=1, price=100, category="base", qty=2)], "SOMECODE"],
    ],
)
def test_base_total(user_id, items, discount_code):
    assert calculate_order_total(user_id, items, discount_code) == 200


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code", "result"],
    [
        [
            2,
            [Item(id=1, price=100, category="electronics", qty=1)],
            "SOMECODE",
            100,
        ],
        [2, [Item(id=1, price=100, category="electronics", qty=1)], None, 100],
        [
            2,
            [Item(id=1, price=100, category="electronics", qty=2)],
            "SOMECODE",
            190,
        ],
        [2, [Item(id=1, price=100, category="electronics", qty=2)], None, 190],
        [
            2,
            [Item(id=1, price=100, category="electronics", qty=10)],
            "SOMECODE",
            950,
        ],
        [
            2,
            [Item(id=1, price=100, category="electronics", qty=10)],
            None,
            950,
        ],
        [
            2,
            [Item(id=1, price=10, category="electronics", qty=1)],
            "SOMECODE",
            10,
        ],
        [2, [Item(id=1, price=10, category="electronics", qty=1)], None, 10],
        [
            2,
            [Item(id=1, price=10, category="electronics", qty=2)],
            "SOMECODE",
            19,
        ],
        [2, [Item(id=1, price=10, category="electronics", qty=2)], None, 19],
        [
            2,
            [Item(id=1, price=10, category="electronics", qty=10)],
            "SOMECODE",
            95,
        ],
        [2, [Item(id=1, price=10, category="electronics", qty=10)], None, 95],
    ],
)
def test_5_percents_sale_electronics(user_id, items, discount_code, result):
    assert calculate_order_total(user_id, items, discount_code) == result


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code", "result"],
    [
        [2, [Item(id=1, price=10, category="books", qty=1)], "SOMECODE", 9],
        [2, [Item(id=1, price=10, category="books", qty=1)], None, 9],
        [2, [Item(id=1, price=10, category="books", qty=10)], "SOMECODE", 90],
        [2, [Item(id=1, price=10, category="books", qty=10)], None, 90],
        [2, [Item(id=1, price=100, category="books", qty=1)], "SOMECODE", 90],
        [2, [Item(id=1, price=100, category="books", qty=1)], None, 90],
        [
            2,
            [Item(id=1, price=100, category="books", qty=10)],
            "SOMECODE",
            900,
        ],
        [2, [Item(id=1, price=100, category="books", qty=10)], None, 900],
    ],
)
def test_10_percents_sale_books(user_id, items, discount_code, result):
    assert calculate_order_total(user_id, items, discount_code) == result


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code", "result"],
    [
        [1, [Item(id=1, price=10, category="base", qty=1)], "SOMECODE", 9],
        [3, [Item(id=1, price=10, category="base", qty=1)], None, 9],
        [1, [Item(id=1, price=10, category="base", qty=10)], "SOMECODE", 90],
        [3, [Item(id=1, price=10, category="base", qty=10)], None, 90],
        [1, [Item(id=1, price=100, category="base", qty=1)], "SOMECODE", 90],
        [3, [Item(id=1, price=100, category="base", qty=1)], None, 90],
        [1, [Item(id=1, price=100, category="base", qty=10)], "SOMECODE", 900],
        [3, [Item(id=1, price=100, category="base", qty=10)], None, 900],
    ],
)
def test_vip_sale(user_id, items, discount_code, result):
    assert calculate_order_total(user_id, items, discount_code) == result


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code", "result"],
    [
        [6, [Item(id=1, price=10, category="base", qty=1)], "SOMECODE", 9.5],
        [8, [Item(id=1, price=10, category="base", qty=1)], None, 9.5],
        [6, [Item(id=1, price=10, category="base", qty=10)], "SOMECODE", 95],
        [8, [Item(id=1, price=10, category="base", qty=10)], None, 95],
        [6, [Item(id=1, price=100, category="base", qty=1)], "SOMECODE", 95],
        [8, [Item(id=1, price=100, category="base", qty=1)], None, 95],
        [6, [Item(id=1, price=100, category="base", qty=10)], "SOMECODE", 950],
        [8, [Item(id=1, price=100, category="base", qty=10)], None, 950],
    ],
)
def test_more_equal_3_years(user_id, items, discount_code, result):
    assert calculate_order_total(user_id, items, discount_code) == result


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code", "result", "month"],
    [
        [
            2,
            [Item(id=1, price=500, category="base", qty=1)],
            "NEWYEAR2025",
            500,
            11,
        ],
        [
            2,
            [Item(id=1, price=500, category="base", qty=1)],
            "NEWYEAR2025",
            0,
            12,
        ],
        [
            2,
            [Item(id=1, price=500, category="base", qty=1)],
            "NEWYEAR2025",
            0,
            1,
        ],
        [
            2,
            [Item(id=1, price=500, category="base", qty=1)],
            "NEWYEAR2025",
            500,
            2,
        ],
        [
            4,
            [Item(id=1, price=5000, category="base", qty=1)],
            "NEWYEAR2025",
            5000,
            11,
        ],
        [
            4,
            [Item(id=1, price=5000, category="base", qty=1)],
            "NEWYEAR2025",
            4500,
            12,
        ],
        [
            4,
            [Item(id=1, price=5000, category="base", qty=1)],
            "NEWYEAR2025",
            4500,
            1,
        ],
        [
            4,
            [Item(id=1, price=5000, category="base", qty=1)],
            "NEWYEAR2025",
            5000,
            2,
        ],
    ],
)
def test_code_new_year(
    monkeypatch, user_id, items, discount_code, result, month
):
    monkeypatch.setattr(
        "src.code_sale.datetime.datetime", make_fake_date(month)
    )
    assert calculate_order_total(user_id, items, discount_code) == result


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code", "result"],
    [
        [2, [Item(id=1, price=100, category="base", qty=1)], "SUMMER", 85],
        [2, [Item(id=1, price=100, category="base", qty=2)], "SUMMER", 170],
        [4, [Item(id=1, price=100, category="base", qty=1)], "SUMMER", 85],
        [4, [Item(id=1, price=100, category="base", qty=2)], "SUMMER", 170],
    ],
)
def test_code_summer(user_id, items, discount_code, result):
    assert calculate_order_total(user_id, items, discount_code) == result


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code"],
    [
        [1, [Item(id=1, price=500, category="base", qty=-1)], "SOMECODE"],
        [2, [Item(id=1, price=500, category="base", qty=-1)], "SOMECODE"],
        [1, [Item(id=1, price=-500, category="base", qty=1)], "SOMECODE"],
        [2, [Item(id=1, price=-500, category="base", qty=1)], "SOMECODE"],
    ],
)
def test_negative_total(user_id, items, discount_code):
    assert calculate_order_total(user_id, items, discount_code) == 0


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code", "month"],
    [
        [2, [Item(id=1, price=50, category="base", qty=1)], "NEWYEAR2025", 12],
        [2, [Item(id=1, price=50, category="base", qty=1)], "NEWYEAR2025", 1],
    ],
)
def test_negative_total_after_newyear_discount(
    monkeypatch, user_id, items, discount_code, month
):
    monkeypatch.setattr(
        "src.code_sale.datetime.datetime", make_fake_date(month)
    )
    assert calculate_order_total(user_id, items, discount_code) == 0


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code", "result"],
    [
        [
            1,
            [Item(id=1, price=500, category="electronics", qty=3)],
            "SOMECODE",
            1282.5,
        ],
        [1, [Item(id=1, price=500, category="books", qty=1)], "SOMECODE", 405],
        [
            6,
            [Item(id=1, price=500, category="electronics", qty=3)],
            "SOMECODE",
            1353.75,
        ],
        [
            6,
            [Item(id=1, price=500, category="books", qty=1)],
            "SOMECODE",
            427.5,
        ],
        [
            1,
            [Item(id=1, price=500, category="electronics", qty=3)],
            "SUMMER",
            1090.125,
        ],
        [
            1,
            [Item(id=1, price=500, category="books", qty=1)],
            "SUMMER",
            344.25,
        ],
        [
            6,
            [Item(id=1, price=500, category="electronics", qty=3)],
            "SUMMER",
            1150.6875,
        ],
        [
            6,
            [Item(id=1, price=500, category="books", qty=1)],
            "SUMMER",
            363.375,
        ],
    ],
)
def test_diff_sale(user_id, items, discount_code, result):
    assert calculate_order_total(user_id, items, discount_code) == result


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code", "result", "month"],
    [
        [
            1,
            [Item(id=1, price=1000, category="electronics", qty=3)],
            "NEWYEAR2025",
            2565.0,
            11,
        ],
        [
            1,
            [Item(id=1, price=1000, category="books", qty=1)],
            "NEWYEAR2025",
            810.0,
            11,
        ],
        [
            6,
            [Item(id=1, price=1000, category="electronics", qty=3)],
            "NEWYEAR2025",
            2707.5,
            11,
        ],
        [
            6,
            [Item(id=1, price=1000, category="books", qty=1)],
            "NEWYEAR2025",
            855.0,
            11,
        ],
        [
            1,
            [Item(id=1, price=1000, category="electronics", qty=3)],
            "NEWYEAR2025",
            2065.0,
            12,
        ],
        [
            1,
            [Item(id=1, price=1000, category="books", qty=1)],
            "NEWYEAR2025",
            310.0,
            12,
        ],
        [
            6,
            [Item(id=1, price=1000, category="electronics", qty=3)],
            "NEWYEAR2025",
            2207.5,
            12,
        ],
        [
            6,
            [Item(id=1, price=1000, category="books", qty=1)],
            "NEWYEAR2025",
            355.0,
            12,
        ],
        [
            1,
            [Item(id=1, price=1000, category="electronics", qty=3)],
            "NEWYEAR2025",
            2065.0,
            1,
        ],
        [
            1,
            [Item(id=1, price=1000, category="books", qty=1)],
            "NEWYEAR2025",
            310.0,
            1,
        ],
        [
            6,
            [Item(id=1, price=1000, category="electronics", qty=3)],
            "NEWYEAR2025",
            2207.5,
            1,
        ],
        [
            6,
            [Item(id=1, price=1000, category="books", qty=1)],
            "NEWYEAR2025",
            355.0,
            1,
        ],
        [
            1,
            [Item(id=1, price=1000, category="electronics", qty=3)],
            "NEWYEAR2025",
            2565.0,
            2,
        ],
        [
            1,
            [Item(id=1, price=1000, category="books", qty=1)],
            "NEWYEAR2025",
            810.0,
            2,
        ],
        [
            6,
            [Item(id=1, price=1000, category="electronics", qty=3)],
            "NEWYEAR2025",
            2707.5,
            2,
        ],
        [
            6,
            [Item(id=1, price=1000, category="books", qty=1)],
            "NEWYEAR2025",
            855.0,
            2,
        ],
    ],
)
def test_diff_sale_new_year(
    monkeypatch, user_id, items, discount_code, result, month
):
    monkeypatch.setattr(
        "src.code_sale.datetime.datetime", make_fake_date(month)
    )
    assert calculate_order_total(user_id, items, discount_code) == result


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code", "result"],
    [
        [
            2,
            [
                Item(id=1, price=100, category="base", qty=1),
                Item(id=2, price=100, category="base", qty=1),
            ],
            "SUMMER",
            170.0,
        ]
    ],
)
def test_summer_discount_applied_once_per_order(
    user_id, items, discount_code, result
):
    assert calculate_order_total(user_id, items, discount_code) == result


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code", "result", "month"],
    [
        [
            2,
            [
                Item(id=1, price=1000, category="base", qty=1),
                Item(id=2, price=1000, category="base", qty=1),
            ],
            "NEWYEAR2025",
            1500,
            12,
        ]
    ],
)
def test_newyear_discount_applied_once_per_order(
    monkeypatch, user_id, items, discount_code, result, month
):
    monkeypatch.setattr(
        "src.code_sale.datetime.datetime", make_fake_date(month)
    )
    assert calculate_order_total(user_id, items, discount_code) == result


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code", "result"],
    [
        [
            1,
            [
                Item(id=1, price=200, category="electronics", qty=2),
                Item(id=2, price=100, category="books", qty=1),
            ],
            None,
            423.0,
        ]
    ],
)
def test_mixed_categories_multi_item_order(
    user_id, items, discount_code, result
):
    assert calculate_order_total(user_id, items, discount_code) == result


@pytest.mark.parametrize(
    ["user_id", "items", "discount_code", "result"],
    [
        [
            2,
            [
                Item(id=1, price=0, category="base", qty=5),
                Item(id=2, price=100, category="base", qty=0),
                Item(id=3, price=50, category="base", qty=2),
            ],
            None,
            100,
        ]
    ],
)
def test_zero_price_or_qty_items_do_not_contribute(
    user_id, items, discount_code, result
):
    assert calculate_order_total(user_id, items, discount_code) == result


@pytest.mark.parametrize(
    ["user_id", "items", "result"],
    [
        [2, [Item(id=1, price=1500, category="base", qty=1)], 1800],
        [2, [Item(id=1, price=2000, category="base", qty=1)], 2300],
        [2, [Item(id=1, price=2500, category="base", qty=1)], 2500],
    ],
)
def test_free_delivery_code(user_id, items, result):
    assert calculate_order_total(user_id, items, "FREEDELIVERY") == result


def test_delivery_code_applied_after_percent_code():
    user_id = 2
    items = [Item(id=1, price=2000, category="base", qty=1)]
    result = calculate_order_total(user_id, items, "SUMMER", "FREEDELIVERY")
    assert result == 2000.0


def test_delivery_code_applied_after_fixed_and_percent_codes(monkeypatch):
    monkeypatch.setattr("src.code_sale.datetime.datetime", make_fake_date(12))
    user_id = 2
    items = [Item(id=1, price=3000, category="base", qty=1)]
    result = calculate_order_total(
        user_id, items, "NEWYEAR2025", "SUMMER", "FREEDELIVERY"
    )
    assert result == 2125.0

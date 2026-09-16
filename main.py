from src.order_calculator import calculate_order_total

if __name__ == "__main__":
    result = calculate_order_total(
        1, [{"id": 1, "price": 100, "category": "electronics", "qty": 2}]
    )
    print(result)

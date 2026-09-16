from src.models import User

# Имитация базы данных в памяти
USERS_DB: dict[int, User] = {
    1: User(name="Иван", registered_years=3, is_vip=True),
    2: User(name="Ольга", registered_years=1, is_vip=False),
    3: User(name="Иван", registered_years=2, is_vip=True),
    4: User(name="Ольга", registered_years=2, is_vip=False),
    5: User(name="Иван", registered_years=3, is_vip=True),
    6: User(name="Ольга", registered_years=3, is_vip=False),
    7: User(name="Иван", registered_years=4, is_vip=True),
    8: User(name="Ольга", registered_years=4, is_vip=False),
}


def get_user_from_db(user_id: int) -> User:
    user: User | None = USERS_DB.get(user_id)
    if not user:
        raise ValueError("User not found")
    return user

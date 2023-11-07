
VALID_EMAIL = "alex@test.net"
VALID_PASSWORD = "12345"

EXPECTED_PET_DATA = {
    "pet": {
        "id": int,
        "name": str,
        "type": str,
        "age": int,
        "gender": str,
        "owner_id": int,
        "pic": str,
        "owner_name": str,
        "likes_count": int,
        "liked_by_user": (int, type(None))  # Поле может быть int или None
    },
    "comments": list  # Ожидается список комментариев
}


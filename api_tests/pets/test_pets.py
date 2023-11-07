from settings import EXPECTED_PET_DATA


def test_get_token(api):
    status = api.get_token()[0]

    assert status == 200, f"Ожидался статус 200, но получен статус {status}"


def test_list_users(api):   # Вместо количества юзеров выводиттся Id Usera
    status, amount = api.get_list_users()

    assert status == 200, f"Ожидался статус 200, но получен статус {status}"
    assert amount is not None


def test_create_pet(api):
    status, token, user_id = api.get_token()  # Получаем user_id для создания питомца
    status, pet_id = api.create_pet(user_id)  # Создаем питомца и получаем его pet_id

    assert status == 200, f"Ожидался статус 200, но получен статус {status}"
    assert pet_id is not None, "Не удалось создать питомца"


def test_send_photo(api):
    status, token, user_id = api.get_token()   # Получаем user_id для создания питомца
    status, pet_id, = api.create_pet(user_id)  # Создаем питомца и получаем его pet_id
    status = api.send_photo(pet_id)

    assert status == 200, f"Ожидался статус 200 при отправке фото питомца, но получен статус {status}"


def test_create_and_delete_user(api, user_data, fake):
    status, token, user_id = api.create_user(user_data)   # Создаем пользователя

    assert status == 200, "Не удалось создать пользователя"

    delete_status = api.delete_user(token, user_id)  # Передаем token и user_id при удалении пользователя

    assert delete_status == 200, "Не удалось удалить пользователя"


def test_get_pet_list(api):
    status, amount = api.pet_list()      # Получаем количество питомцев

    assert status == 200, "Не удалось получить список"
    assert amount is not None


def test_get_pet(api):
    status, token, user_id = api.get_token()  # Получаем user_id для создания питомца
    status, pet_id = api.create_pet(user_id)  # Создаем питомца и получаем его pet_id
    pet_data = api.get_pet(pet_id)            # Получаем данные о питомце

    assert isinstance(pet_data, dict), "Фактические данные не соответствуют ожидаемой структуре"
    assert all(key in pet_data for key in EXPECTED_PET_DATA)


def test_delete_pet(api):
    status, token, user_id = api.get_token()  # Получаем user_id для создания питомца
    status, pet_id = api.create_pet(user_id)  # Создаем питомца и получаем его pet_id
    delete_status = api.delete_pet(pet_id)    # Удаляем питомца

    assert delete_status == 200, "Не удалось удалить питомца"


def test_pet_update(api):
    status, token, user_id = api.get_token()  # Получаем user_id для создания питомца
    status, pet_id = api.create_pet(user_id)  # Создаем питомца и получаем его pet_id
    # Новые данные для обновления питомца
    update_data = {
        "id": pet_id,
        "name": "Garfild",
        "type": "cat",
        "age": 4,
    }
    api.pet_update(pet_id, update_data)        # Обновление информации о питомце
    updated_pet_data = api.get_pet(pet_id)     # Получение информации о питомце

    assert updated_pet_data["pet"]["name"] == "Garfild", "Имя питомца не было обновлено"
    assert updated_pet_data["pet"]["type"] == "cat", "Тип питомца не был обновлен"
    assert updated_pet_data["pet"]["age"] == 4, "Возраст питомца не был обновлен"


def test_add_like(api):
    status, token, user_id = api.get_token()  # Получаем user_id для создания питомца
    status, pet_id = api.create_pet(user_id)  # Создаем питомца и получаем его pet_id
    result1 = api.add_like(pet_id)            # Попробуем добавить лайк и проверим результат

    assert result1 == "Лайк успешно добавлен", "Ошибка: Лайк не был успешно добавлен"


def test_add_comment(api):

    status, token, user_id = api.get_token()   # Получаем user_id для создания питомца
    status, pet_id = api.create_pet(user_id)   # Создаем питомца и получаем его pet_id

    # Добавляем комментарий к питомцу
    comment_text = "I like this monster)"
    status, comment_id = api.add_comment(pet_id, comment_text)
    pet_data = api.get_pet(pet_id)             # Получаем инфрмацию о питомце
    comments = pet_data.get("comments", [])    # Получаем значения ключа
    comment_texts = [comment["message"] for comment in comments]    # Создаем список с коментариями

    assert comment_text in comment_texts, "Комментарий не был добавлен"
    assert status == 200, f"Ожидался статус 200, но получен статус {status}"
    assert comment_id is not None, "Не удалось добавить комментарий"

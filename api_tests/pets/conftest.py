import pytest
from api.api_pet import API
from faker import Faker


@pytest.fixture
def api():
    return API()   # Добавляем класс в фикстуру


@pytest.fixture
def fake():
    fake = Faker()  # Создаем объект Faker
    return fake


@pytest.fixture
def user_data(fake):  # Генерируем данные для нового юзера
    password = fake.password()
    user_data = {
        "email": fake.email(),
        "password": password,
        "confirm_password": password
    }
    return user_data


@pytest.fixture()
def user_token():
    user_api = API()
    token = user_api.get_token()
    return token



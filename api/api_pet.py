import requests
import json
from settings import VALID_EMAIL, VALID_PASSWORD


class API:
    """ API библиотека к сайту http://34.141.58.52:8080/#/"""
    def __init__(self):
        self.base_url = 'http://34.141.58.52:8000/'
        self.token = None
        self.user_id = None

    def get_token(self):
        """ Получает токен пользователя, либо возвращает его, если уже получен"""
        if self.token:
            return self.token

        try:
            email = VALID_EMAIL
            password = VALID_PASSWORD
            data = {"email": email, "password": password}
            res = requests.post(self.base_url + 'login', data=json.dumps(data))
            res.raise_for_status()
            self.token = res.json()['token']
            self.user_id = res.json()['id']
            status = res.status_code
            return status, self.token, self.user_id
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе токена: {e}")

    def create_user(self, user_data):
        """ Создает нового пользователя с заданными данными"""
        try:
            res = requests.post(self.base_url + 'register', data=json.dumps(user_data))
            res.raise_for_status()
            user_id = res.json().get('id')
            token = res.json().get('token')
            status = res.status_code
            return status, token, user_id
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе: {e}")

    def get_list_users(self):
        """ Получает список пользователей"""
        try:
            token = self.get_token()[1]
            headers = {'Authorization': f'Bearer {token}'}
            res = requests.get(self.base_url + 'users', headers=headers)
            res.raise_for_status()
            users = res.json()
            status = res.status_code
            return status, users
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе: {e}")

    def delete_user(self, token, user_id):
        """ Удаляет пользователя с заданным токеном и идентификатором"""
        try:
            headers = {'Authorization': f'Bearer {token}'}
            res = requests.delete(self.base_url + f'users/{user_id}', headers=headers)
            res.raise_for_status()
            delete_status = res.status_code
            return delete_status
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при выполнении запроса: {e}")

    def create_pet(self, user_id):
        """ Создает нового питомца для заданного пользователя"""
        try:
            token = self.get_token()
            headers = {'Authorization': f'Bearer {token}'}
            data = {
                    "name": 'CoopeR',
                    "type": 'dog',
                    "age": 3,
                    "gender": "male",
                    "owner_id": user_id
                    }
            res = requests.post(self.base_url + 'pet', data=json.dumps(data), headers=headers)
            res.raise_for_status()
            status = res.status_code
            pet_id = res.json().get('id')
            return status, pet_id
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе: {e}")

    def send_photo(self, pet_id):
        """ Отправляет фотографию для питомца с заданным идентификатором"""
        try:
            token = self.get_token()
            headers = {'Authorization': f'Bearer {token}'}
            files = {'pic': ('pet.jpg',
                             open(r'C:\Users\freed\PycharmProjects\API_Tests_Pets\api_tests\pets\photo\pet.jpg', 'rb'),
                             'image/jpeg')}
            res = requests.post(self.base_url + f'pet/{pet_id}/image', headers=headers, files=files)
            res.raise_for_status()
            status = res.status_code
            return status
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе: {e}")

    def get_pet(self, pet_id):
        """ Получает информацию о питомце с заданным идентификатором"""
        try:
            token = self.get_token()
            headers = {'Authorization': f'Bearer {token}'}
            res = requests.get(self.base_url + f'pet/{pet_id}', headers=headers)
            res.raise_for_status()
            pet_data = res.json()
            return pet_data
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе: {e}")

    def pet_list(self):
        """ Получает список питомцев"""
        try:
            status, token, owner_id = self.get_token()  # Получаем статус, токен и идентификатор пользователя
            headers = {'Authorization': f'Bearer {token}'}
            body = {
                "skip": 0,
                "num": 10,
                "type": "string",
                "petName": "string",
                "user_id": owner_id
            }
            res = requests.post(self.base_url + 'pets', data=json.dumps(body), headers=headers)
            res.raise_for_status()
            amount = res.json()
            status = res.status_code
            print(amount)
            return status, amount
        except requests.exceptions.RequestException as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return None

    def delete_pet(self, pet_id):
        """ Удаляет питомца с заданным идентификатором"""
        try:
            token = self.get_token()
            headers = {'Authorization': f'Bearer {token}'}
            res = requests.delete(self.base_url + f'pet/{pet_id}', headers=headers)
            res.raise_for_status()
            status = res.status_code
            return status
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе: {e}")

    def pet_update(self, pet_id, update_data):
        """ Обновляет информацию о питомце с заданным идентификатором"""
        try:
            token = self.get_token()
            headers = {'Authorization': f'Bearer {token}'}
            update_data["id"] = pet_id
            res = requests.patch(self.base_url + f'pet', headers=headers, data=json.dumps(update_data))
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе: {e}")

    def add_like(self, pet_id):
        """ Добавляет лайк для питомца с заданным идентификатором"""
        try:
            token = self.get_token()
            headers = {'Authorization': f'Bearer {token}'}
            res = requests.put(self.base_url + f'pet/{pet_id}/like', headers=headers)
            res.raise_for_status()
            if res.status_code == 200:
                result = "Лайк успешно добавлен"
            elif res.status_code == 403 and "You already liked it" in res.text:
                result = "Вы уже поставили лайк этому питомцу"
            else:
                result = "Не удалось добавить лайк"
            return result
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе: {e}")

    def add_comment(self, pet_id, comment_text):
        """ Добавляет комментарий для питомца с заданным идентификатором"""
        try:
            token = self.get_token()
            headers = {'Authorization': f'Bearer {token}'}
            data = {"message": comment_text}
            res = requests.put(self.base_url + f'pet/{pet_id}/comment', data=json.dumps(data), headers=headers)
            res.raise_for_status()
            status = res.status_code
            comment_id = res.json().get('id')
            return status, comment_id
        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе: {e}")

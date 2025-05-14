


import requests
from data.urls import Urls

class ApiClient:
    def __init__(self):
        self.base_url = Urls.BASE
        self.session = requests.Session()

    def register_user(self, email, password, name):
        """Регистрация пользователя."""
        url = f"{self.base_url}/api/auth/register"  # Добавьте '/api' в URL
        data = {
            "email": email,
            "password": password,
            "name": name
        }
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response

    def login(self, email, password):
        """Авторизация пользователя"""
        url = f"{self.base_url}/api/auth/login"
        data = {"email": email, "password": password}
        return self.session.post(url, json=data)

    def delete_user(self, access_token):
        """Удаление пользователя"""
        url = f"{self.base_url}/api/auth/user"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.session.delete(url, headers=headers)
        response.raise_for_status()
        return response

    def create_order(self, ingredients, access_token):
        url = f"{self.base_url}/api/orders"
        data = {"ingredients": ingredients}
        headers = {"Authorization": f"Bearer {access_token}"}
        response = self.session.post(url, headers=headers, json=data)  # Исправлено на self.session
        response.raise_for_status()
        return response.json()

    def get_ingredients(self):
        url = f'{self.base_url}/api/ingredients'
        response = requests.get(url)
        response.raise_for_status()
        return response
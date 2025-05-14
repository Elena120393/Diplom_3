import pytest
import requests
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from helpers.api_client import ApiClient
from helpers.generate_data import generate_email
from data.urls import Urls
from pages.login_page import LoginPage
from pages.main_page import MainPage


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome",
                     help="Выбор браузера: chrome или firefox")
    parser.addoption("--chrome-driver", action="store",
                     default="C:\\WebDrivers\\chromedriver.exe",
                     help="Полный путь к chromedriver.exe")
    parser.addoption("--firefox-driver", action="store",
                     default="C:\\WebDrivers\\geckodriver.exe",
                     help="Полный путь к geckodriver.exe")


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser").lower()
    chrome_driver_path = request.config.getoption("--chrome-driver")
    firefox_driver_path = request.config.getoption("--firefox-driver")

    driver = None

    try:
        if browser == "chrome":
            if not os.path.exists(chrome_driver_path):
                pytest.fail(f"ChromeDriver не найден по пути: {chrome_driver_path}")

            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            service = ChromeService(executable_path=chrome_driver_path)
            driver = webdriver.Chrome(service=service, options=options)

        elif browser == "firefox":
            if not os.path.exists(firefox_driver_path):
                pytest.fail(f"GeckoDriver не найден по пути: {firefox_driver_path}")

            options = webdriver.FirefoxOptions()
            options.add_argument("--start-maximized")
            service = FirefoxService(executable_path=firefox_driver_path)
            driver = webdriver.Firefox(service=service, options=options)

        else:
            raise pytest.UsageError("--browser должен быть chrome или firefox")

        yield driver

    except Exception as e:
        pytest.fail(f"Ошибка инициализации {browser}: {str(e)}")

    finally:
        if driver:
            driver.quit()

@pytest.fixture
def api_client():
    return ApiClient()

@pytest.fixture
def test_user(api_client):
    """Фикстура создания тестового пользователя"""
    email = generate_email()
    password = "ValidPassword123!"
    name = "Test User"

    # Регистрация
    reg_response = api_client.register_user(email, password, name)
    reg_response.raise_for_status()
    access_token = reg_response.json()['accessToken']

    yield {
        "email": email,
        "password": password,
        "name": name,
        "access_token": access_token
    }

    # Удаление после теста
    try:
        api_client.delete_user(access_token)
    except requests.exceptions.HTTPError as e:
        print(f"Ошибка удаления пользователя: {str(e)}")

@pytest.fixture
def logged_in_user(driver, test_user):
    login_page = LoginPage(driver)
    login_page.open()

    # Выполняем вход
    login_page.enter_email(test_user["email"])
    login_page.enter_password(test_user["password"])
    login_page.click_login_button()

    # Ждем перехода на главную страницу
    WebDriverWait(driver, 15).until(
        EC.url_to_be(Urls.MAIN),
        message="Не удалось войти в систему"
    )

    # Получаем токен
    access_token = driver.execute_script(
        "return localStorage.getItem('accessToken');"
    )
    if not access_token:
        pytest.fail("Токен не найден")
    return {"access_token": access_token.replace("Bearer ", "")}

@pytest.fixture
def main_page(driver):
    """Фикстура для работы с главной страницей"""
    return MainPage(driver)

@pytest.fixture
def test_order(api_client, test_user):
    """Фикстура создания тестового заказа"""
    try:
        # Получаем ингредиенты через API
        ingredients_response = api_client.get_ingredients()
        ingredients_response.raise_for_status()
        ingredients_data = ingredients_response.json()["data"]

        # Выбираем валидные ингредиенты
        valid_ingredients = [ingredient["_id"] for ingredient in ingredients_data[:2]]

        # Создаем заказ
        order_response = api_client.create_order(
            ingredients=valid_ingredients,
            access_token=test_user["access_token"]
        )
        order_response.raise_for_status()
        yield order_response.json()

    except Exception as e:
        pytest.fail(f"Ошибка создания заказа: {e}")
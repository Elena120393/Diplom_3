

import pytest
import allure
from pages.login_page import LoginPage
from pages.account_page import AccountPage
from pages.header_page import HeaderPage
from data.test_data import TestData



@allure.feature('Личный кабинет')
class TestAccount:
    @allure.title('Переход в личный кабинет после авторизации')
    def test_navigate_to_account(self, driver, logged_in_user):
        login_page = LoginPage(driver)
        account_page = login_page.click_account_button()
        assert account_page.is_profile_opened(), "Страница профиля не открылась"

    @allure.title('Проверка истории заказов')
    def test_order_history(self, driver):
        login_page = LoginPage(driver)
        header = HeaderPage(driver)
        account_page = AccountPage(driver)

        # Шаг 1: Авторизация
        with allure.step("Авторизоваться"):
            login_page.open()
            login_page.login(TestData.VALID_EMAIL, TestData.VALID_PASSWORD)
            assert header.is_profile_button_visible(), "Не удалось авторизоваться"

        # Шаг 2: Переход в личный кабинет
        with allure.step("Перейти в личный кабинет"):
            header.open_profile()

        # Шаг 3: Проверка истории заказов
        with allure.step("Кликнуть на 'История заказов'"):
            account_page.navigate_to_order_history()

        with allure.step("Проверить переход в раздел истории заказов"):
            assert "account/order-history" in driver.current_url, "Не перешли в историю заказов"
            assert account_page.has_order_history(), "История заказов не отображается"

    @allure.title('Выход из аккаунта')
    def test_logout(self, driver, logged_in_user):
        account_page = AccountPage(driver)
        login_page = LoginPage(driver)

        with allure.step("Перейти в личный кабинет и выйти"):
            account_page.logout()

        with allure.step("Проверить переход на страницу входа"):
            assert login_page.is_login_page_opened(), "Выход не выполнен"


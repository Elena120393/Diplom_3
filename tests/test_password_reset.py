


import allure
import pytest
import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
from helpers.generate_data import generate_email
from pages.login_page import LoginPage
from pages.forgot_password_page import ForgotPasswordPage
from data.test_data import TestData
from data.urls import Urls
from selenium.webdriver.common.by import By

logger = logging.getLogger(__name__)


@allure.feature("Восстановление пароля")
class TestForgotPassword:
    """Тесты для функционала восстановления пароля."""

    @allure.title("Переход на страницу восстановления пароля")
    def test_navigate_to_recovery_page(self, driver):
        login_page = LoginPage(driver)

        with allure.step("Открыть страницу входа"):
            login_page.open()

        with allure.step("Кликнуть на кнопку 'Личный кабинет'"):
            login_page.click(login_page.locators.ACCOUNT_BUTTON)

        with allure.step("Дождаться загрузки страницы логина"):
            login_page.wait_for_visibility(login_page.locators.EMAIL_INPUT)

        with allure.step("Проверить URL страницы логина"):
            assert driver.current_url == Urls.LOGIN, f"Ожидался URL {Urls.LOGIN}, получен {driver.current_url}"

        with allure.step("Кликнуть на ссылку 'Восстановить пароль'"):
            login_page.click(login_page.locators.FORGOT_PASSWORD_LINK)

        with allure.step("Дождаться загрузки страницы восстановления пароля"):
            recovery_page = ForgotPasswordPage(driver)
            recovery_page.wait_for_visibility(recovery_page.locators.RESTORE_BUTTON)

        with allure.step("Проверить URL страницы восстановления пароля"):
            assert driver.current_url == Urls.FORGOT_PASSWORD, \
                f"Ожидался URL {Urls.FORGOT_PASSWORD}, получен {driver.current_url}"

        with allure.step("Проверить наличие основных элементов на странице"):
            assert recovery_page.is_element_visible(
                recovery_page.locators.RESTORE_BUTTON), "Кнопка восстановления не отображается"
            assert recovery_page.is_element_visible(recovery_page.locators.EMAIL_INPUT), "Поле email не отображается"

    @allure.title("Отправка формы восстановления")
    def test_submit_recovery_form(self, driver):
        page = ForgotPasswordPage(driver)
        page.go_to_forgot_password_page()

        email = generate_email()
        page.input_text(page.locators.EMAIL_INPUT, email)

        # Проверка подсветки поля после ввода
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(page.locators.ACTIVE_FIELD)
        )
        assert page.is_element_visible(page.locators.ACTIVE_FIELD), "Поле email не подсвечено"

        page.click_element(page.locators.RESTORE_BUTTON)

        try:
            WebDriverWait(driver, 10).until(
                EC.url_contains("reset-password")
            )
        except TimeoutException:
            driver.save_screenshot("recovery_failed.png")
            logger.error("Форма восстановления не была отправлена")
            pytest.fail("Не произошло перехода на страницу сброса пароля")

    @allure.title("Проверка работы кнопки показа пароля")
    def test_show_password_button(self, driver):
        login_page = LoginPage(driver)
        login_page.open()

        login_page.enter_email(TestData.VALID_EMAIL)
        login_page.enter_password(TestData.VALID_PASSWORD)

        password_field = login_page.find_element(login_page.locators.PASSWORD_INPUT)
        assert password_field.get_attribute("type") == "password"

        # Клик по кнопке показа пароля
        login_page.click(login_page.locators.SHOW_PASSWORD_BUTTON)

        # Проверка подсветки поля (ищем родительский элемент)
        parent_element = password_field.find_element(By.XPATH, "./..")
        assert "input_status_active" in parent_element.get_attribute("class"), "Поле пароля не подсвечено"

        # Проверка отображения пароля
        WebDriverWait(driver, 5).until(
            lambda _: password_field.get_attribute("type") == "text"
        )


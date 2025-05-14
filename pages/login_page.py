




from locators.login_page_locators import LoginPageLocators
from pages.base_page import BasePage
from pages.account_page import AccountPage
from data.urls import Urls
import allure


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = LoginPageLocators()


    @allure.step("Открыть страницу входа")
    def open(self):
        self.driver.get(Urls.LOGIN)
        self.wait_for_visibility(LoginPageLocators.EMAIL_INPUT)
        return self

    @allure.step("Ввести email: {email}")
    def enter_email(self, email):
        self.input_text(LoginPageLocators.EMAIL_INPUT, email)
        return self

    @allure.step("Ввести пароль: {password}")
    def enter_password(self, password):
        self.input_text(LoginPageLocators.PASSWORD_INPUT, password)
        return self

    @allure.step("Кликнуть по кнопке 'Войти'")
    def click_login_button(self):
        self.wait_for_clickable(LoginPageLocators.LOGIN_BUTTON, timeout=30)  # Увеличено до 30 сек
        self.click(LoginPageLocators.LOGIN_BUTTON)
        return self


    @allure.step("Перейти на страницу регистрации")
    def navigate_to_register(self):
        self.click(LoginPageLocators.REGISTER_LINK)
        self.wait_for_url_contains(Urls.REGISTER)
        return self

    @allure.step("Перейти на страницу восстановления пароля")
    def navigate_to_forgot_password(self):
        self.click(LoginPageLocators.FORGOT_PASSWORD_LINK)
        self.wait_for_url_contains(Urls.FORGOT_PASSWORD)
        return self

    @allure.step("Проверить наличие ошибки валидации")
    def is_validation_error_visible(self):
        return self.is_element_visible(LoginPageLocators.ERROR_MESSAGE)

    @allure.step("Получить текст ошибки валидации")
    def get_validation_error_text(self):
        return self.get_text(LoginPageLocators.ERROR_MESSAGE)

    @allure.step("Проверить успешный вход")
    def is_login_successful(self):
        return self.wait_for_url_contains(Urls.MAIN)

    @allure.step("Проверить открытие страницы входа")
    def is_login_page_opened(self):
        return self.wait_for_url_contains(Urls.LOGIN)

    @allure.step("Кликнуть по кнопке 'Личный кабинет'")
    def click_account_button(self):
        self.click(LoginPageLocators.ACCOUNT_BUTTON)
        return AccountPage(self.driver)


    def go_to_login_page(self):
        self.open()
        return self

    @allure.step("Выполнить вход с email: {email} и паролем: {password}")
    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        return AccountPage(self.driver)
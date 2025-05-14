


from selenium.common.exceptions import TimeoutException
import logging
from .base_page import BasePage
from locators.forgot_password_page_locators import ForgotPasswordLocators
from data.urls import Urls
import allure

logger = logging.getLogger(__name__)

class ForgotPasswordPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.locators = ForgotPasswordLocators()
        self.urls = Urls()

    @allure.step("Перейти на страницу восстановления пароля")
    def go_to_forgot_password_page(self):
        self.driver.get(self.urls.FORGOT_PASSWORD)
        if not self.is_element_visible(self.locators.EMAIL_INPUT, timeout=10):
            logger.error("Forgot password page failed to load")
            self.driver.save_screenshot("forgot_password_page_error.png")
            raise TimeoutException("Страница восстановления пароля не загрузилась")
        return self

    @allure.step("Кликнуть на кнопку 'Показать пароль'")
    def click_show_password_button(self):
        self.click_element(self.locators.SHOW_PASSWORD_BUTTON)
        return self

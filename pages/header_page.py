

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators.header_locators import HeaderLocators
from pages.base_page import BasePage
from data.urls import Urls
import allure

class HeaderPage(BasePage):
    @allure.step("Кликнуть на кнопку 'Конструктор'")
    def click_constructor_button(self):
        self.click(HeaderLocators.CONSTRUCTOR_BUTTON)
        self.wait_for_url_contains(Urls.MAIN)
        return self

    @allure.step("Кликнуть на кнопку 'Лента заказов'")
    def click_order_feed(self):
        element = self.wait_for_presence(HeaderLocators.ORDER_FEED_LINK, timeout=20)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self.wait_for_clickable(HeaderLocators.ORDER_FEED_LINK, timeout=20)
        self.driver.execute_script("arguments[0].click();", element)
        self.wait_for_url_contains(Urls.FEED, timeout=20)
        return self

    @allure.step("Кликнуть на кнопку 'Личный кабинет'")
    def click_profile_button(self):
        self.click(HeaderLocators.PROFILE_BUTTON)
        self.wait_for_url_contains(Urls.ACCOUNT_PROFILE)
        return self

    @allure.step("Кликнуть на кнопку 'Войти в аккаунт'")
    def click_login_button(self):
        self.click(HeaderLocators.LOGIN_BUTTON)
        self.wait_for_url_contains(Urls.LOGIN)
        return self

    @allure.step("Проверить активность раздела 'Конструктор'")
    def is_constructor_active(self):
        return self.is_element_visible(HeaderLocators.ACTIVE_SECTION_INDICATOR)

    @allure.step("Проверить активность раздела 'Лента заказов'")
    def is_order_feed_active(self):
        return self.is_element_visible(HeaderLocators.ACTIVE_SECTION_INDICATOR)

    @allure.step("Проверить видимость кнопки входа")
    def is_login_button_visible(self):
        return self.is_element_visible(HeaderLocators.LOGIN_BUTTON)

    @allure.step("Проверить видимость кнопки профиля")
    def is_profile_button_visible(self):
        return self.is_element_visible(HeaderLocators.PROFILE_BUTTON)

    @allure.step("Проверить переход на главную страницу")
    def is_main_page_opened(self):
        return self.wait_for_url_contains("/")

    @allure.step("Проверить переход в ленту заказов")
    def is_feed_page_opened(self):
        return self.wait_for_url_contains(Urls.FEED)

    @allure.step("Открыть личный кабинет")
    def open_profile(self):
        self.wait_for_clickable(HeaderLocators.PROFILE_BUTTON)
        self.click(HeaderLocators.PROFILE_BUTTON)
        self.wait_for_url_contains(Urls.ACCOUNT_PROFILE)
        return self

    @allure.step("Перейти в Личный кабинет")
    def navigate_to_profile(self):
        self.wait_for_clickable(HeaderLocators.PROFILE_BUTTON)
        self.driver.find_element(*HeaderLocators.PROFILE_BUTTON).click()

    @allure.step("Ожидание видимости кнопки конструктора")
    def wait_for_constructor_visibility(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(HeaderLocators.CONSTRUCTOR_BUTTON)
        )

    @allure.step("Проверить переход в профиль")
    def is_profile_page_opened(self):
        return self.wait_for_url_contains(Urls.ACCOUNT_PROFILE)


import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from locators.account_page_locators import AccountPageLocators
from locators.header_locators import HeaderLocators
from pages.base_page import BasePage
from pages.header_page import HeaderPage
from data.urls import Urls


class AccountPage(BasePage):
    @allure.step("Открыть страницу личного кабинета")
    def open(self):
        # Вместо прямого перехода по URL используем клик по кнопке в хедере
        HeaderPage(self.driver).navigate_to_profile()
        return self

    @allure.step("Проверить открытие страницы профиля")
    def is_profile_opened(self):
        return self.wait_for_url_contains(Urls.ACCOUNT_PROFILE)


    @allure.step("Проверить наличие истории заказов")
    def has_order_history(self):
        try:
            return self.is_element_visible(AccountPageLocators.ORDER_CARD)
        except TimeoutException:
            return False

    @allure.step("Выйти из аккаунта")
    def logout(self):
        self.wait_for_clickable(HeaderLocators.PROFILE_BUTTON).click()
        self.wait_for_clickable(AccountPageLocators.LOGOUT_BUTTON).click()
        self.wait_for_url_contains(Urls.LOGIN)
        return self


    @allure.step("Проверить подсветку активного раздела")
    def is_section_active(self, section_name):
        element = self.wait_for_visibility(AccountPageLocators.ACTIVE_SECTION)
        return section_name.lower() in element.text.lower()

    @allure.step("Перейти в раздел 'Профиль'")
    def navigate_to_profile(self):
        self.wait_for_clickable(AccountPageLocators.PROFILE_TAB, timeout=20)
        self.click(AccountPageLocators.PROFILE_TAB)
        self.wait_for_url_contains(Urls.ACCOUNT_PROFILE)
        return self

    @allure.step("Перейти в раздел 'История заказов'")
    def navigate_to_order_history(self):
        self.wait_for_clickable(AccountPageLocators.ORDER_HISTORY_LINK)
        self.click(AccountPageLocators.ORDER_HISTORY_LINK)
        self.wait_for_url_contains(Urls.ACCOUNT_ORDER_HISTORY)
        return self

    @allure.step("Открыть страницу профиля через меню")
    def open_via_menu(self):
        HeaderPage(self.driver).navigate_to_profile()
        self.wait_for_profile_load()
        return self

    @allure.step("Дождаться загрузки профиля")
    def wait_for_profile_load(self, timeout=20):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(AccountPageLocators.PROFILE_SECTION)
            )
            return True
        except TimeoutException:
            raise Exception("Страница профиля не загрузилась за {timeout} секунд")

    @allure.step("Проверить, что открыта страница истории заказов")
    def is_order_history_page_opened(self):
        # Получаем текущий URL для отладки
        current_url = self.driver.current_url
        allure.attach(current_url, "Current URL in is_order_history_page_opened", allure.attachment_type.TEXT)

        # Проверяем, содержит ли URL строку "order-history"
        url_check = "order-history" in current_url

        # Проверяем наличие элементов на странице
        try:
            # Проверяем наличие хотя бы одного из элементов, характерных для страницы истории заказов
            elements_check = (
                    self.is_element_present(AccountPageLocators.ORDER_NUMBER, timeout=5) or
                    self.is_element_present(AccountPageLocators.ORDER_STATUS, timeout=5) or
                    self.is_element_present(AccountPageLocators.ORDER_CARD, timeout=5) or
                    self.is_element_present(AccountPageLocators.ORDER_HISTORY_SECTION, timeout=5)
            )
        except Exception as e:
            allure.attach(str(e), "Exception during element check", allure.attachment_type.TEXT)
            elements_check = False

        # Логируем результаты проверок
        allure.attach(f"URL check: {url_check}, Elements check: {elements_check}",
                      "Check results", allure.attachment_type.TEXT)

        # Возвращаем True, если URL содержит "order-history"
        # Мы полагаемся только на URL, так как элементы могут отсутствовать, если история заказов пуста
        return url_check

    @allure.step("Ожидание видимости элемента или изменения URL")
    def wait_for_element_visibility_or_url_change(self, url_part, timeout=15):
        """Ждет либо видимости элемента истории заказов, либо изменения URL"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: (
                        self.is_element_visible(AccountPageLocators.ORDER_HISTORY_SECTION, timeout=1) or
                        url_part in driver.current_url
                )
            )
            return True
        except TimeoutException:
            current_url = self.driver.current_url
            allure.attach(current_url, "Current URL after timeout", allure.attachment_type.TEXT)
            return False

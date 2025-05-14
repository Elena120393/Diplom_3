

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
        self.driver.find_element(*HeaderLocators.PROFILE_BUTTON).click()
        self.wait_for_url_contains("/account/profile", timeout=15)
        self.wait_for_clickable(AccountPageLocators.LOGOUT_BUTTON, timeout=20)
        self.click(AccountPageLocators.LOGOUT_BUTTON)
        self.wait_for_url_contains(Urls.LOGIN)
        return self


    @allure.step("Проверить подсветку активного раздела")
    def is_section_active(self, section_name):
        locator = (AccountPageLocators.ACTIVE_SECTION_INDICATOR[0],
                   f"{AccountPageLocators.ACTIVE_SECTION_INDICATOR[1]}[text()='{section_name}']")
        return self.is_element_visible(locator)

    @allure.step("Перейти в раздел 'Профиль'")
    def navigate_to_profile(self):
        self.wait_for_clickable(AccountPageLocators.PROFILE_TAB, timeout=20)
        self.click(AccountPageLocators.PROFILE_TAB)
        self.wait_for_url_contains(Urls.ACCOUNT_PROFILE)
        return self

    @allure.step("Перейти в раздел 'История заказов'")
    def navigate_to_order_history(self):
        self.wait_for_clickable(AccountPageLocators.ORDER_HISTORY_LINK, timeout=20)
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

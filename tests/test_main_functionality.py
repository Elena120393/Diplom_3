

import allure
from pages.header_page import HeaderPage
from pages.feed_page import FeedPage
from locators.feed_locators import FeedPageLocators


@allure.feature("Хедер")
class TestHeader:
    @allure.title("Переход в конструктор из ленты заказов")
    def test_navigate_to_constructor_from_feed(self, driver):
        feed = FeedPage(driver).open()
        header = HeaderPage(driver)
        header.click_constructor_button()
        assert header.is_main_page_opened(), "Не перешли в конструктор"

    @allure.title("Переход в ленту заказов из конструктора")
    def test_navigate_to_feed_from_constructor(self, driver):
        feed = FeedPage(driver).open()
        feed.wait_for_element_visible(FeedPageLocators.FEED_SECTION, timeout=20)
        assert feed.is_feed_page_opened(), "Не перешли в ленту заказов"

    @allure.title("Переход в личный кабинет после авторизации")
    def test_navigate_to_profile_authorized(self, logged_in_user, driver):
        header = HeaderPage(driver)
        header.open_profile()
        assert header.is_profile_page_opened(), "Не перешли в профиль"

    @allure.title("Отображение кнопки 'Личный кабинет' для авторизованного пользователя")
    def test_profile_button_visibility_for_user(self, logged_in_user, driver):
        header = HeaderPage(driver)
        assert header.is_profile_button_visible(), "Кнопка профиля не видна"
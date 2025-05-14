
from pages.main_page import MainPage
from locators.main_page_locators import MainPageLocators
from data.urls import Urls
import allure


@allure.feature("Конструктор бургеров")
class TestBurgerConstructor:
    @allure.title("Отображение модального окна с деталями ингредиента")
    def test_ingredient_modal_open(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()

        with allure.step("Кликнуть на первый ингредиент"):
            main_page.click_first_ingredient()

        with allure.step("Проверить открытие модального окна"):
            assert main_page.is_ingredient_modal_visible(), "Модальное окно не открылось"

        with allure.step("Проверить заголовок модального окна"):
            expected_title = "Детали ингредиента"
            actual_title = main_page.get_modal_title()
            assert actual_title == expected_title, f"Заголовок окна: '{actual_title}' вместо '{expected_title}'"

    @allure.title("Закрытие модального окна с деталями ингредиента")
    def test_ingredient_modal_open_close(self, driver):
        main_page = MainPage(driver)
        main_page.open_main_page()

        # Открытие модального окна
        with allure.step("Кликнуть на первый ингредиент"):
            main_page.click_first_ingredient()

        with allure.step("Проверить открытие модального окна"):
            assert main_page.is_ingredient_modal_visible(), "Модальное окно не открылось"

        with allure.step("Проверить заголовок модального окна"):
            expected_title = "Детали ингредиента"
            actual_title = main_page.get_modal_title()
            assert actual_title == expected_title, f"Заголовок окна: '{actual_title}' вместо '{expected_title}'"

        # Закрытие модального окна
        with allure.step("Закрыть модальное окно кликом по крестику"):
            main_page.close_modal()

        with allure.step("Проверить закрытие модального окна"):
            assert main_page.is_ingredient_modal_closed(), "Модальное окно не закрылось"
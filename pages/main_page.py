



from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import allure

from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators
from data.urls import Urls

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver, Urls.MAIN)

    @allure.step("Добавить булку '{bun_name}' в конструктор")
    def drag_bun_to_constructor(self, bun_name: str):
        bun_img = self.wait_for_visibility(
            MainPageLocators.bun_image_by_name(bun_name), timeout=20
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", bun_img)
        target = self.wait_for_visibility(MainPageLocators.CONSTRUCTOR_AREA)
        ActionChains(self.driver).drag_and_drop(bun_img, target).perform()
        self.wait_for_visibility(
            MainPageLocators.constructor_element_with_name(bun_name),
            timeout=10
        )
        return self

    @allure.step("Добавить начинку '{filling_name}' в конструктор")
    def add_filling_to_constructor(self, filling_name: str):
        # переключаем вкладку с начинками
        self.click(MainPageLocators.FILLINGS_TAB)
        section = self.wait_for_visibility(MainPageLocators.FILLINGS_SECTION)
        filling_img = self.wait_for_visibility(
            MainPageLocators.filling_image_by_name(filling_name), timeout=20
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", filling_img)
        target = self.wait_for_visibility(MainPageLocators.CONSTRUCTOR_AREA)
        ActionChains(self.driver).drag_and_drop(filling_img, target).perform()
        self.wait_for_visibility(
            MainPageLocators.constructor_element_with_name(filling_name),
            timeout=10
        )
        return self

    @allure.step("Добавить соус '{sauce_name}' в конструктор")
    def add_sauce_to_constructor(self, sauce_name: str):
        # переключаем вкладку с соусами
        self.click(MainPageLocators.SAUCES_TAB)
        section = self.wait_for_visibility(MainPageLocators.SAUCES_SECTION)
        sauce_img = self.wait_for_visibility(
            MainPageLocators.sauce_image_by_name(sauce_name), timeout=20
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", sauce_img)
        target = self.wait_for_visibility(MainPageLocators.CONSTRUCTOR_AREA)
        ActionChains(self.driver).drag_and_drop(sauce_img, target).perform()
        self.wait_for_visibility(
            MainPageLocators.constructor_element_with_name(sauce_name),
            timeout=10
        )
        return self

    @allure.step("Оформить заказ")
    def place_order(self):
        btn = self.wait_for_clickable(MainPageLocators.ORDER_BUTTON)
        btn.click()
        return self

    @allure.step("Дождаться открытия модального окна заказа")
    def wait_for_order_modal(self, timeout: int = 20):
        # Ждём появления контейнера модального окна и игнорируем возвращаемое WebElement
        self.wait_for_visibility(MainPageLocators.ORDER_MODAL, timeout=timeout)
        return self


    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        try:
            close_btn = self.wait_for_clickable(MainPageLocators.CLOSE_MODAL_BUTTON, timeout=5)
            close_btn.click()
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(MainPageLocators.ORDER_MODAL)
            )
        except Exception:
            ActionChains(self.driver).send_keys("\uE00C").perform()  # ESC key
            WebDriverWait(self.driver, 5).until(
                EC.invisibility_of_element_located(MainPageLocators.ORDER_MODAL)
            )
        return self

    @allure.step("Получить номер заказа из модального окна")
    def get_order_number_from_modal(self):
        try:
            WebDriverWait(self.driver, 20).until(
                lambda d: d.find_element(*MainPageLocators.ORDER_MODAL_TITLE).text != '9999'
            )
            order_number_element = self.wait_for_visibility(
                MainPageLocators.ORDER_MODAL_TITLE,
                timeout=10
            )
            return order_number_element.text
        except Exception as e:
            allure.attach(
                self.driver.get_screenshot_as_png(),
                name="order_number_error",
                attachment_type=allure.attachment_type.PNG
            )
            raise AssertionError(f"Не удалось получить номер заказа из модального окна: {str(e)}")

    @allure.step("Проверить наличие ингредиента '{ingredient_name}' в конструкторе")
    def is_ingredient_in_constructor(self, ingredient_name: str) -> bool:
        locator = MainPageLocators.constructor_element_with_name(ingredient_name)
        return self.is_element_present(locator, timeout=5)


    @allure.step("Ожидать, пока счётчик ингредиента превысит {initial_value}")
    def wait_for_counter_increase(self, initial_value: int, timeout: int = 10) -> int:
        """
        Явно ждём, пока любой из видимых счётчиков станет больше initial_value.
        Возвращаем новое значение.
        """

        def _counter_updated(driver):
            els = driver.find_elements(*MainPageLocators.INGREDIENT_COUNTER)
            for el in els:
                if el.is_displayed() and el.text.isdigit():
                    val = int(el.text)
                    if val > initial_value:
                        return val
            return False

        return WebDriverWait(self.driver, timeout).until(_counter_updated)

    @allure.step("Кликнуть на ингредиент '{name}'")
    def click_ingredient(self, name):
        locator = MainPageLocators.INGREDIENT_ITEM_BY_NAME(name)
        self.click(locator)
        return self

    @allure.step("Проверить видимость модального окна")
    def is_modal_visible(self):
        return self.is_element_visible(MainPageLocators.INGREDIENT_MODAL)

    @allure.step("Закрыть модальное окно")
    def close_modal(self):
        self.click(MainPageLocators.MODAL_CLOSE_BUTTON)
        return self

    @allure.step("Проверить закрытие модального окна")
    def is_modal_closed(self):
        return self.is_element_invisible(MainPageLocators.INGREDIENT_MODAL)

    def open_main_page(self):
        self.driver.get(Urls.MAIN)
        return self

    @allure.step("Кликнуть на первый ингредиент")
    def click_first_ingredient(self):
        self.click(MainPageLocators.FIRST_INGREDIENT)
        return self

    @allure.step("Проверить видимость модального окна")
    def is_ingredient_modal_visible(self):
        return self.wait_for_visibility(MainPageLocators.INGREDIENT_MODAL, timeout=10)

    @allure.step("Получить заголовок модального окна")
    def get_modal_title(self):
        return self.get_text(MainPageLocators.MODAL_TITLE)

    @allure.step("Проверить закрытие модального окна")
    def is_ingredient_modal_closed(self):
        return self.is_element_invisible(MainPageLocators.INGREDIENT_MODAL)





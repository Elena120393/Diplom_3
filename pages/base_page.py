

import functools
import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException
)
from selenium.webdriver import ActionChains


class BasePage:
    def __init__(self, driver, url=None):
        self.driver = driver
        self.base_url = url
        self.wait = WebDriverWait(driver, 15)
        self.actions = ActionChains(driver)  # Инициализация ActionChains

    @allure.step("Открыть страницу")
    def open(self):
        if self.base_url:
            self.driver.get(self.base_url)
        return self

    @allure.step("Кликнуть по элементу {locator}")
    def click(self, locator, timeout=15):
        def _click():
            element = self.wait_for_clickable(locator, timeout)
            element.click()
            return True

        try:
            return _click()
        except StaleElementReferenceException:
            return self.wait_for_clickable(locator, timeout).click()

    @allure.step("Ожидать кликабельности элемента")
    def wait_for_clickable(self, locator, timeout=15):
        return self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент {locator} не стал кликабельным за {timeout} сек"
        )

    @allure.step("Найти элемент {locator}")
    def find_element(self, locator, timeout=15):
        try:
            return self.wait.until(
                EC.presence_of_element_located(locator)
            )
        except TimeoutException:
            raise NoSuchElementException(f"Элемент не найден: {locator}")

    @allure.step("Ввести текст '{text}' в поле {locator}")
    def input_text(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)
        return self

    @allure.step("Получить текст элемента {locator}")
    def get_text(self, locator):
        return self.wait.until(
            EC.visibility_of_element_located(locator)
        ).text

    @allure.step("Проверить видимость элемента {locator}")
    def is_visible(self, locator, timeout=5):
        try:
            self.wait.until(
                EC.visibility_of_element_located(locator),
                timeout=timeout
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Перетащить элемент {source_locator} на {target_locator}")
    def drag_and_drop(self, source_locator, target_locator):
        source = self.find_element(source_locator)
        target = self.find_element(target_locator)
        self.actions.drag_and_drop(source, target).perform()
        return self

    @allure.step("Получить атрибут '{attribute}' элемента {locator}")
    def get_attribute(self, locator, attribute):
        return self.wait.until(
            EC.presence_of_element_located(locator)
        ).get_attribute(attribute)

    @allure.step("Ожидать изменения URL")
    def wait_for_url_change(self, initial_url):
        self.wait.until(lambda d: d.current_url != initial_url)
        return self

    @allure.step("Обновить страницу")
    def refresh(self):
        self.driver.refresh()
        return self

    @allure.step("Проверить текущий URL")
    def current_url_contains(self, expected_part):
        return expected_part in self.driver.current_url

    @allure.step("Выполнить JavaScript-скрипт")
    def execute_script(self, script, element=None):
        if element:
            self.driver.execute_script(script, element)
        else:
            self.driver.execute_script(script)
        return self

    @allure.step("Ожидание URL, содержащего {expected_part}")
    def wait_for_url_contains(self, expected_part, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.url_contains(expected_part)
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Очистить и ввести текст")
    def clear_and_send_keys(self, locator, text):
        element = self.wait_for_clickable(locator)
        element.clear()
        element.send_keys(text)
        return self

    @allure.step("Ожидание видимости всех элементов {locator}")
    def wait_for_all_visible(self, locator, timeout=10):
        return self.wait.until(
            EC.visibility_of_all_elements_located(locator)
        )

    @allure.step("Ожидание исчезновения элемента {locator}")
    def wait_for_invisibility(self, locator, timeout=10):
        return self.wait.until(
            EC.invisibility_of_element_located(locator)
        )

    @allure.step("Прокрутить к элементу {locator}")
    def scroll_to_element(self, locator):
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView()", element)
        return self

    @allure.step("Проверить наличие элемента")
    def is_element_present(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    @staticmethod
    def handle_exceptions(error_message):  # Убрали self
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    raise Exception(f"{error_message}: {str(e)}") from e

            return wrapper

        return decorator

    @allure.step("Проверить видимость элемента")
    def is_element_visible(self, locator, timeout=5):
        try:
            self.wait_for_visibility(locator, timeout)
            return True
        except TimeoutException:
            return False

    @allure.step("Ожидать исчезновения элемента")
    def wait_for_element_invisible(self, locator, timeout=10):
        return self.wait.until(
            EC.invisibility_of_element_located(locator),
            message=f"Элемент {locator} не скрылся за {timeout} сек"
        )

    @allure.step("Кликнуть по элементу")
    def click_element(self, locator, timeout=10):
        element = self.wait_for_clickable(locator, timeout)
        element.click()

    @allure.step("Ожидать видимости элемента")
    def wait_for_visibility(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator),
            message=f"Элемент {locator} не отобразился за {timeout} сек"
        )

    @allure.step("Ожидать кликабельности элемента")
    def wait_for_clickable(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator),
            message=f"Элемент {locator} не стал кликабельным за {timeout} сек"
        )

    def wait_for_element_present(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def wait_for_presence(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator),
            message=f"Элемент {locator} не появился в DOM за {timeout} сек"
        )

    def is_element_invisible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False


from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from locators.feed_locators import FeedPageLocators
from pages.base_page import BasePage
import time
from data.urls import Urls
import allure
from locators.main_page_locators import MainPageLocators  # Добавлен импорт

class FeedPage(BasePage):

    @allure.step("Проверить видимость списка заказов")
    def is_order_list_visible(self):
        try:
            return self.wait_for_visibility(FeedPageLocators.ORDER_LIST)
        except TimeoutException:
            return False

    @allure.step("Клик по первому заказу в ленте")
    def click_first_order(self):
        element = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable(FeedPageLocators.FIRST_ORDER_IN_LIST)
        )
        self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Получить номер заказа из модального окна")
    def get_order_number_from_modal(self):
        return self.wait_for_visibility(FeedPageLocators.MODAL_ORDER_NUMBER).text

    @allure.step("Получить общее количество выполненных заказов")
    def get_total_orders_count(self):
        text = self.wait_for_visibility(FeedPageLocators.TOTAL_ORDERS_COUNTER).text
        counter_digits = ''.join(filter(str.isdigit, text))
        return int(counter_digits)

    @allure.step("Получить количество заказов за сегодня")
    def get_today_orders_count(self):
        text = self.wait_for_visibility(FeedPageLocators.TODAY_ORDERS_COUNTER).text
        counter_digits = ''.join(filter(str.isdigit, text))
        return int(counter_digits)

    @allure.step("Проверить наличие заказа в работе")
    def is_order_in_progress(self, order_number):
        try:
            orders = self.wait_for_all_visible(FeedPageLocators.IN_PROGRESS_ORDER_NUMBERS)
            return any(order_number in order.text for order in orders)
        except TimeoutException:
            return False

    @allure.step("Закрыть модальное окно деталей заказа")
    def close_order_details_modal(self):
        self.wait_for_clickable(FeedPageLocators.MODAL_CLOSE_BUTTON).click()
        self.wait_for_invisibility(FeedPageLocators.ORDER_DETAILS_MODAL, timeout=10)
        return self

    @allure.step("Дождаться обновления счетчика заказов")
    def wait_for_counter_increase(self, initial_value: int, counter_type: str = 'total', timeout: int = 40) -> bool:
        locator = FeedPageLocators.TOTAL_ORDERS_COUNTER if counter_type == 'total' else FeedPageLocators.TODAY_ORDERS_COUNTER

        def _counter_updated(driver):
            counter_text = driver.find_element(*locator).text
            counter_digits = ''.join(filter(str.isdigit, counter_text))
            current_val = int(counter_digits)
            return current_val > initial_value

        try:
            return WebDriverWait(self.driver, timeout).until(_counter_updated)
        except TimeoutException:
            counter_text = self.driver.find_element(*locator).text
            counter_digits = ''.join(filter(str.isdigit, counter_text))
            current_value = int(counter_digits)
            raise AssertionError(
                f"Счетчик не увеличился. Изначальное значение: {initial_value}, текущее: {current_value}"
            )

    @allure.step("Проверить видимость модального окна заказа")
    def is_order_modal_visible(self):
        try:
            return self.wait_for_visibility(FeedPageLocators.ORDER_DETAILS_MODAL, timeout=15) is not None
        except TimeoutException:
            return False

    @allure.step("Ожидание видимости элемента")
    def wait_for_element_visible(self, locator, timeout=10):
        return self.wait_for_visibility(locator, timeout=timeout)

    @allure.step("Проверить наличие заказа в ленте по номеру")
    def click_first_order(self):
        elem = self.wait_for_clickable(FeedPageLocators.FIRST_ORDER_IN_LIST)
        self.driver.execute_script("arguments[0].click();", elem)
        return self

    @allure.step("Открыть страницу ленты заказов")
    def open(self):
        self.driver.get(Urls.FEED)
        self.wait_for_visibility(FeedPageLocators.FEED_SECTION, timeout=30)
        return self

    @allure.step("Проверить, что модальное окно закрыто")
    def is_order_modal_closed(self):
        try:
            return self.wait_for_invisibility(FeedPageLocators.ORDER_DETAILS_MODAL, timeout=10)
        except TimeoutException:
            return False

    @allure.step('Открытие страницы ленты заказов')
    def open_feed_page(self):
        self.open()

    @allure.step('Проверка открытия модального окна')
    def is_modal_opened(self):
        try:
            self.wait_for_element_visible(FeedPageLocators.COMPOSITION_HEADER)
            return True
        except TimeoutException:
            return False

    @allure.step('Ожидание появления заказа {order_number} в списке "В работе"')
    def wait_for_order_in_progress(self, order_number, timeout=10):
        self.wait_for_orders_to_load()
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.is_order_in_progress(order_number):
                return True
        return False

    @allure.step('Ожидание загрузки списка заказов')
    def wait_for_orders_to_load(self):
        self.wait_for_element_visible(FeedPageLocators.ORDER_LIST)

    @allure.step('Получение списка заказов в работе')
    def get_in_progress_orders(self):
        elems = self.driver.find_elements(*FeedPageLocators.IN_PROGRESS_ORDER_NUMBERS)
        return [e.text.strip().lstrip('#') for e in elems]

    @allure.step("Получить список номеров в секции 'Готовы'")
    def get_done_orders(self):
        elems = self.driver.find_elements(*FeedPageLocators.DONE_ORDER_NUMBERS)
        return [e.text.strip().lstrip('#') for e in elems]

    @allure.step('Поиск элементов {locator}')
    def find_elements(self, locator, timeout=None):
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        try:
            return wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []

    @allure.step("Дождаться появления заказа {order_number}")
    def wait_for_order_to_show(self, order_number: str, timeout: int = 30) -> bool:
        def _order_in_list(driver):
            in_prog = self.get_in_progress_orders()
            done = self.get_done_orders()
            return order_number in in_prog or order_number in done

        return WebDriverWait(self.driver, timeout).until(_order_in_list)


    @allure.step("Дождаться видимости конструктора")
    def wait_for_constructor_visibility(self, timeout=10):
        return self.wait_for_visibility(MainPageLocators.CONSTRUCTOR_AREA, timeout)

    @allure.step("Проверить наличие заказа {order_number} в ленте")
    def is_order_in_list(self, order_number):
        orders = self.driver.find_elements(*FeedPageLocators.ORDER_NUMBER_IN_LIST)
        for order in orders:
            order_num_text = order.text.strip().lstrip('#').lstrip('0')
            if str(order_number) == order_num_text:
                return True
        return False
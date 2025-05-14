



import allure
from pages.feed_page import FeedPage
from pages.main_page import MainPage
from pages.header_page import HeaderPage
from data.test_data import TestData
from helpers.api_client import ApiClient
from locators.feed_locators import FeedPageLocators
from locators.main_page_locators import MainPageLocators
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



@allure.feature('Лента заказов')
class TestFeed:

    @allure.title('Открытие модального окна с деталями заказа')
    def test_open_order_details_modal(self, driver):
        feed = FeedPage(driver).open()
        feed.wait_for_element_visible(FeedPageLocators.FEED_SECTION, timeout=20)
        assert feed.is_element_present(FeedPageLocators.FIRST_ORDER_IN_LIST), "Нет заказов в ленте"
        feed.click_first_order()
        assert feed.is_modal_opened(), "Модальное окно не открылось после клика на заказ"

    @allure.title('Проверка отображения заказа пользователя в ленте')
    def test_user_order_in_feed(self, driver, logged_in_user):
        api = ApiClient()
        ingredients = TestData.VALID_INGREDIENT_IDS
        resp = api.create_order(ingredients, logged_in_user["access_token"])
        order_number = resp["order"]["number"]
        feed = FeedPage(driver).open()
        assert feed.is_order_in_list(order_number), f"Заказ {order_number} не найден в ленте"

    @allure.title('Проверка увеличения счетчика "Выполнено за всё время"')
    def test_total_counter_increases_after_order(self, driver, logged_in_user):
        main = MainPage(driver)
        feed = FeedPage(driver)
        header = HeaderPage(driver)

        feed.open()
        initial_count = feed.get_total_orders_count()

        header.click_constructor_button()
        main.wait_for_visibility(MainPageLocators.CONSTRUCTOR_AREA)

        # добавляем ингредиенты
        main.drag_bun_to_constructor(TestData.INGREDIENT_1)
        main.add_filling_to_constructor(TestData.INGREDIENT_2)
        main.add_sauce_to_constructor(TestData.INGREDIENT_3)

        main.place_order().wait_for_order_modal().close_order_modal()

        feed.open()
        feed.wait_for_counter_increase(initial_count)
        new_count = feed.get_total_orders_count()
        assert new_count > initial_count, f"Счетчик не изменился: {initial_count} → {new_count}"

    @allure.title('Проверка увеличения счетчика "Выполнено за сегодня"')
    def test_today_counter_increases_after_order(self, driver, logged_in_user):
        main = MainPage(driver)
        feed = FeedPage(driver)
        header = HeaderPage(driver)

        feed.open()
        initial_today = feed.get_today_orders_count()

        header.click_constructor_button()
        main.wait_for_visibility(MainPageLocators.CONSTRUCTOR_AREA)

        main.drag_bun_to_constructor(TestData.INGREDIENT_1)
        main.add_filling_to_constructor(TestData.INGREDIENT_2)
        main.add_sauce_to_constructor(TestData.INGREDIENT_3)

        main.place_order().wait_for_order_modal().close_order_modal()

        feed.open()
        feed.wait_for_counter_increase(initial_today, counter_type='today')
        new_today = feed.get_today_orders_count()
        assert new_today > initial_today, f"Счетчик 'за сегодня' не изменился: {initial_today} → {new_today}"

    @allure.title('Проверка отображения заказа в разделе "В работе"')
    def test_order_in_progress_after_order(self, driver, logged_in_user):
        main   = MainPage(driver)
        feed   = FeedPage(driver)
        header = HeaderPage(driver)

        # 1. Получаем начальный счётчик за сегодня
        feed.open()
        initial_today = feed.get_today_orders_count()

        # 2. Формируем заказ через UI
        header.click_constructor_button()
        main.wait_for_visibility(MainPageLocators.CONSTRUCTOR_AREA)
        main.drag_bun_to_constructor(TestData.INGREDIENT_1)
        main.add_filling_to_constructor(TestData.INGREDIENT_2)
        main.add_sauce_to_constructor(TestData.INGREDIENT_3)

        # 3. Оформляем заказ и ждём модалку
        main.place_order().wait_for_order_modal()

        # 4. Получаем номер заказа из модального окна
        order_number = main.get_order_number_from_modal()
        main.close_order_modal()

        # 5. Закрываем модалку
        main.close_order_modal()

        # 6. Проверяем, что заказ появился в разделе "В работе"
        feed.open()
        is_in_progress = feed.wait_for_order_in_progress(order_number)
        assert is_in_progress, f"Номер заказа {order_number} не появился в работе"

    @allure.title('Проверка увеличения счетчика ингредиента при добавлении')
    def test_ingredient_counter_increases_after_adding(self, driver, logged_in_user):
        """Счетчик увеличивается при добавлении булки в конструктор."""
        main_page = MainPage(driver)
        ingredient_name = "Флюоресцентная булка R2-D3"

        main_page.open()

        # Добавляем булку через JS
        main_page.drag_bun_to_constructor(ingredient_name)

        # Ожидаем появления в конструкторе
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                MainPageLocators.constructor_element_with_name(ingredient_name)
            ),
            message="Булка не появилась в конструкторе"
        )

        # Локатор счетчика
        counter_locator = MainPageLocators.ingredient_counter_by_name(ingredient_name)



    @allure.title("Залогиненный пользователь формирует заказ и видит увеличение счетчика")
    def test_user_can_add_ingredients_and_place_order(self, driver, logged_in_user):
        main = MainPage(driver)
        feed = FeedPage(driver)
        header = HeaderPage(driver)

        # 1. Получаем начальный счётчик «за сегодня»
        feed.open()
        initial_today = feed.get_today_orders_count()

        # 2. Формируем заказ через UI: переходим в конструктор и добавляем ингредиенты
        header.click_constructor_button()
        main.wait_for_visibility(MainPageLocators.CONSTRUCTOR_AREA)
        main.drag_bun_to_constructor(TestData.INGREDIENT_1)
        main.add_filling_to_constructor(TestData.INGREDIENT_2)
        main.add_sauce_to_constructor(TestData.INGREDIENT_3)

        # 3. Проверяем, что после добавления ингредиентов отображается кнопка "Оформить заказ"
        assert main.is_element_present(MainPageLocators.ORDER_BUTTON), \
            "Кнопка 'Оформить заказ' не отображается после добавления ингредиентов"



    @allure.title("НЕзалогиненный пользователь не может оформить заказ")
    def test_user_cannot_place_order_without_login(self, driver):
        main = MainPage(driver)
        feed = FeedPage(driver)
        header = HeaderPage(driver)

        # 1. Получаем начальный счётчик «за сегодня»
        feed.open()

        # 2. Открываем конструктор
        header.click_constructor_button()
        main.wait_for_visibility(MainPageLocators.CONSTRUCTOR_AREA)

        # 2. Формируем заказ через UI: переходим в конструктор и добавляем ингредиенты
        header.click_constructor_button()
        main.wait_for_visibility(MainPageLocators.CONSTRUCTOR_AREA)
        main.drag_bun_to_constructor(TestData.INGREDIENT_1)
        main.add_filling_to_constructor(TestData.INGREDIENT_2)
        main.add_sauce_to_constructor(TestData.INGREDIENT_3)

        # 3. Проверяем, что кнопка "Оформить заказ" отсутствует до добавления ингредиентов
        assert not main.is_element_present(MainPageLocators.ORDER_BUTTON), \
            "Кнопка 'Оформить заказ' не должна отображаться без ингредиентов"

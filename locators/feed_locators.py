




from selenium.webdriver.common.by import By

class FeedPageLocators:
    # Основные элементы ленты
    FEED_SECTION = (By.XPATH, "//section[contains(@class, 'OrderFeed')] | //div[contains(@class, 'OrderFeed')]")
    ORDER_LIST = (By.XPATH, "//ul[contains(@class, 'OrderFeed_list__')]")

    # Отдельные заказы
    ORDER_NUMBER_IN_LIST = (By.XPATH, "//p[contains(@class, 'text_type_digits-default') and starts-with(text(), '#')]")

    # Модальное окно заказа
    #ORDER_DETAILS_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__container')]")
    ORDER_DETAILS_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal') and contains(@class, 'opened')]")


    MODAL_ORDER_NUMBER = (By.XPATH, ".//h2[contains(@class, 'text_type_digits-large')]")
    MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, "button.Modal_modal__close_modified__3V5XS")

    # Счетчики заказов
    TOTAL_ORDERS_COUNTER = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p")
    TODAY_ORDERS_COUNTER = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p")

    # Заказы в работе
    IN_PROGRESS_SECTION = (By.XPATH, "//div[contains(@class, 'OrderFeed_inProgress__')]")
    IN_PROGRESS_ORDER_NUMBERS = (By.XPATH, ".//li[contains(@class, 'text_type_digits-default')]")

    ORDER_NUMBERS_WITH_DEFAULT_STYLE = (By.CSS_SELECTOR, ".text_type_digits-default.mb-2")

    # Статус заказа
    ORDER_STATUS = (By.XPATH, ".//span[contains(@class, 'OrderFeed_status__')]")
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal_opened__')]")

    COMPOSITION_HEADER = (By.XPATH, "//p[contains(@class, 'text_type_main-medium') and normalize-space()='Cостав']")

    TODAY_COUNTER = (By.XPATH, "//p[contains(text(),'Выполнено за сегодня')]/following-sibling::p")

    # Сайдбар: Выполнено за всё время и за сегодня
    TOTAL_COUNTER = (By.XPATH, "//p[text()='Выполнено за все время']/following-sibling::p")


    # Сайдбар: статусы «Готовы» и «В работе»
    DONE_SECTION_TITLE = (By.XPATH, "//div[contains(text(),'Готовы')]")
    IN_PROGRESS_SECTION_TITLE = (By.XPATH, "//div[contains(text(),'В работе')]")
    DONE_ORDER_NUMBERS = (By.XPATH, "//div[contains(text(),'Готовы')]/following-sibling::ul//li")

    # Модальное окно заказа
    MODAL = (By.XPATH, "//div[contains(@class,'Modal_modal__container')]")
    CLOSE_BUTTON = (By.XPATH, "//button[contains(@class,'Modal_modal__close')]")

    # Специальный локатор для проверки открытого модала деталей
    MODAL_CONTENT = (By.XPATH, "//div[@class='OrderDetails']")

    # Локация первой записи в ленте
    FIRST_ORDER_IN_LIST = (By.CSS_SELECTOR, "a[href^='/feed/']:first-child")

    # Динамический локатор для поиска заказа по номеру
    @staticmethod
    def order_in_list_by_number(order_number: str):
        return (
            By.XPATH,
            f"//a[contains(@href, '/feed/') and .//p[text()='{order_number}']]"
        )
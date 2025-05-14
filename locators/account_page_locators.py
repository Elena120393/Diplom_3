

from selenium.webdriver.common.by import By


class AccountPageLocators:
    # Основные элементы
    PROFILE_SECTION = (By.CLASS_NAME, "Account_account__3DXMI")
    SUCCESS_MESSAGE = (By.XPATH, "//p[contains(@class, 'notification_status_ok')]")

    # Навигация
    ORDER_HISTORY_LINK = (By.XPATH, "//a[@href='/account/order-history']")
    LOGOUT_BUTTON = (By.XPATH, "//button[contains(@class, 'Account_button__14Yp3') and text()='Выход']")

    # Поля профиля
    NAME_FIELD = (By.XPATH, "//input[@name='name']")
    EMAIL_FIELD = (By.XPATH, "//input[@name='email']")
    PASSWORD_FIELD = (By.XPATH, "//input[@name='password']")

    # Кнопки действий
    SAVE_BUTTON = (By.XPATH, "//button[text()='Сохранить']")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(), 'Отмена')]")

    # Валидация
    ERROR_MESSAGE = (By.XPATH, "//p[contains(@class, 'input__error')]")

    # История заказов
    ORDER_CARD = (By.CLASS_NAME, "OrderHistory_textBox__3lgbs")
    ORDER_NUMBER = (By.XPATH, ".//p[contains(@class, 'text_type_digits-default')]")

    ACTIVE_SECTION_INDICATOR = (By.XPATH, "//div[contains(@class, 'tab_tab_type_current')]")

    PROFILE_TAB = (By.XPATH, "//a[@href='/account/profile' and contains(@class, 'Account_link__')]")
    ORDER_HISTORY_TAB = (By.XPATH, "//a[@href='/account/order-history' and contains(@class, 'Account_link__')]")

    # Локатор активного раздела
    ACTIVE_SECTION = (By.XPATH, "//div[contains(@class, 'Account_link_active__')]")
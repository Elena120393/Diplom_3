

from selenium.webdriver.common.by import By


class HeaderLocators:
    # Основные элементы хедера
    CONSTRUCTOR_BUTTON = (By.XPATH, "//a[.//p[text()='Конструктор'] and contains(@href, '/')]")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента Заказов']/ancestor::a")
    LOGIN_BUTTON = (By.XPATH, "//button[.//p[text()='Войти в аккаунт']]")
    PROFILE_BUTTON = (By.XPATH, "//a[.//p[contains(text(), 'Личный Кабинет')]]")

    # Индикаторы активного раздела
    ACTIVE_SECTION_INDICATOR = (By.XPATH, "//div[contains(@class, 'AppHeader_header__link_active__1IkJo')]")

    # Логотип
    LOGO = (By.XPATH, "//div[contains(@class, 'AppHeader_header__logo__')]")

    ORDER_FEED_LINK = (By.XPATH, "//a[.//p[text()='Лента заказов']]")

    PERSONAL_ACCOUNT_BUTTON = (By.XPATH, "//a[contains(@class, 'AppHeader_header__link') and @href='/account']")
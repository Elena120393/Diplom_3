
from selenium.webdriver.common.by import By


class LoginPageLocators:
    # Основные элементы
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[name='name']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Войти')]")

    # Навигация
    REGISTER_LINK = (By.CSS_SELECTOR, "a[href^='/register']")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a[href^='/forgot-password']")

    # Валидация
    ERROR_MESSAGE = (By.CSS_SELECTOR, "p.input__error")
    EMPTY_EMAIL_ERROR = (By.XPATH, "//p[text()='Введите email']")
    EMPTY_PASSWORD_ERROR = (By.XPATH, "//p[text()='Введите пароль']")

    # Статус страницы
    PAGE_HEADER = (By.XPATH, "//h2[text()='Вход']")
    LOADER = (By.CSS_SELECTOR, "div.loader")

    ACCOUNT_BUTTON = (By.XPATH, "//a[contains(@href, '/account')]")

    SHOW_PASSWORD_BUTTON = (By.CSS_SELECTOR, "div.input__icon")

    ACTIVE_FIELD = (By.CSS_SELECTOR, "div.input_status_active")

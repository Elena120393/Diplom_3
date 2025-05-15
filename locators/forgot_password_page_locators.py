




from selenium.webdriver.common.by import By

class ForgotPasswordLocators:
    # Поля ввода
    EMAIL_INPUT = (By.CSS_SELECTOR, "input.text.input__textfield.text_type_main-default[name='name']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input.text.input__textfield.text_type_main-default[name='Пароль']")
    CODE_INPUT = (By.XPATH, "//input[@name='token']")

    # Кнопки
    RESTORE_BUTTON = (By.XPATH, "//button[contains(text(), 'Восстановить')]")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(), 'Сохранить')]")
    SHOW_PASSWORD_BUTTON = (By.CSS_SELECTOR, "div.input__icon")

    # Ссылки
    LOGIN_LINK = (By.XPATH, "//a[text()='Войти']")

    # Индикаторы состояния
    ACTIVE_FIELD = (By.XPATH, "//div[contains(@class, 'input_status_active')]")

    # Сообщения об ошибках
    ERROR_MESSAGE = (By.XPATH, "//*[contains(text(), 'Ошибка')]")


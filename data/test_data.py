

class TestData:
    # Валидные данные для авторизации
    VALID_EMAIL = "elena_artemeva_19_789@gmail.com"
    VALID_PASSWORD = "elena_artemeva_19_789@gmail.com"
    DEFAULT_NAME = "Test User"

    # Невалидные данные для тестов
    INVALID_EMAIL = "invalid_email@test..com"
    INVALID_PASSWORD = "12345"
    EMPTY_FIELD = ""

    # Данные для восстановления пароля
    RESET_EMAIL = "elena_artemeva_19_789@gmail.com"
    RESET_CODE =  "elena_artemeva_19_789@gmail.com"

    # Тестовые ингредиенты
    INGREDIENT_1 = "Флюоресцентная булка R2-D3"
    INGREDIENT_2 = "Мясо бессмертных моллюсков Protostomia"
    INGREDIENT_3 = "Соус Spicy-X"

    # Тексты ошибок
    ERROR_MESSAGES = {
        "invalid_credentials": "Неверный логин или пароль",
        "empty_email": "Введите email",
        "empty_password": "Введите пароль"
    }

    # Тексты интерфейса
    UI_TEXT = {
        "order_section_title": "Лента заказов",
        "profile_section_title": "Профиль"
    }

    VALID_INGREDIENT_IDS = [
        "61c0c5a71d1f82001bdaaa6d",  # Флюоресцентная булка R2-D3
        "61c0c5a71d1f82001bdaaa6f"  # Мясо бессмертных моллюсков Protostomia
    ]




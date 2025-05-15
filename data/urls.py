

class Urls:
    # Базовый URL приложения
    BASE = "https://stellarburgers.nomoreparties.site"

    # Основные разделы
    MAIN            = f"{BASE}/"
    LOGIN           = f"{BASE}/login"
    REGISTER        = f"{BASE}/register"
    FORGOT_PASSWORD = f"{BASE}/forgot-password"
    RESET_PASSWORD  = f"{BASE}/reset-password"
    FEED            = f"{BASE}/feed"

    # Личный кабинет (UI)
    ACCOUNT_PROFILE       = f"{BASE}/account"
    ACCOUNT_ORDER_HISTORY = f"{BASE}/account/orders"

    # API эндпоинты
    API_BASE     = f"{BASE}/api"
    API_REGISTER = f"{API_BASE}/auth/register"
    API_LOGIN    = f"{API_BASE}/auth/login"
    API_USER     = f"{API_BASE}/auth/user"
    API_ORDER    = f"{BASE}/api/orders"

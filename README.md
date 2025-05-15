# Автоматизированное тестирование Stellar Burgers

Проект автоматизированного тестирования веб-приложения Stellar Burgers (https://stellarburgers.nomoreparties.site/).

## Описание проекта

Проект содержит автоматизированные тесты для проверки основного функционала сайта Stellar Burgers:
- Авторизация и регистрация пользователей
- Восстановление пароля
- Работа с личным кабинетом
- Конструктор бургеров
- Лента заказов
- Оформление заказов

## Технологии

- Python 3.8+
- Selenium WebDriver
- Pytest
- Allure Reports
- Page Object Model

## Структура проекта

Diplom_3/
├── conftest.py (уже предоставлен)
├── requirements.txt (уже предоставлен)
├── data/
│   ├── urls.py
│   └── test_data.py
├── helpers/
│   └── user_generator.py
├── locators/
│   ├── main_page_locators.py
│   ├── login_page_locators.py
│   ├── register_page_locators.py
│   ├── profile_page_locators.py
│   ├── feed_page_locators.py
│   └── order_details_locators.py
├── pages/
│   ├── base_page.py
│   ├── main_page.py
│   ├── login_page.py
│   ├── register_page.py
│   ├── forgot_password_page.py
│   ├── profile_page.py
│   ├── feed_page.py
│   └── order_details_page.py
└── tests/
    ├── test_login.py
    ├── test_register.py
    ├── test_forgot_password.py
    ├── test_profile.py
    ├── test_constructor.py
    └── test_feed.py
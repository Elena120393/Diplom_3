


from selenium.webdriver.common.by import By

class MainPageLocators:
    # Секции фильтров

    SAUCES_SECTION        = (By.XPATH, "//h2[text()='Соусы']/parent::div")
    FILLINGS_SECTION      = (By.XPATH, "//h2[text()='Начинки']/parent::div")

    # Таб-кнопки
    BUNS_TAB              = (By.XPATH, "//span[text()='Булки']/parent::div")
    SAUCES_TAB            = (By.XPATH, "//span[text()='Соусы']/parent::div")
    FILLINGS_TAB          = (By.XPATH, "//span[text()='Начинки']/parent::div")

    # Общий список ингредиентов
    INGREDIENT_ITEM       = (By.CSS_SELECTOR, "div.BurgerIngredient_ingredient__wrapper")
    INGREDIENT_NAME       = (By.CSS_SELECTOR, "p.BurgerIngredient_name__text")
    INGREDIENT_COUNTER    = (By.XPATH, ".//div[contains(@class, 'counter_counter__num__')]")

    # Конструктор
    CONSTRUCTOR_AREA      = (By.XPATH, "//div[contains(@class, 'BurgerConstructor_basket')]")
    CONSTRUCTOR_ROW       = (By.XPATH, "//div[contains(@class,'BurgerConstructor_basket')]/div[contains(@class,'row')]")

    # Кнопки и ссылки
    ORDER_BUTTON            = (By.XPATH, "//button[text()='Оформить заказ']")
    PERSONAL_ACCOUNT_LINK   = (By.XPATH, "//a[@href='/account']")
    CLOSE_MODAL_BUTTON      = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")

    # Модальное окно заказа и номер заказа
    ORDER_MODAL           = (By.XPATH, "//div[contains(@class,'Modal_modal__container')]")
    ORDER_NUMBER          = (By.XPATH, "//div[contains(@class,'order-number')]")

    INGREDIENT_ITEM_BY_NAME = lambda name: (
    By.XPATH, f"//div[contains(@class, 'BurgerIngredient_ingredient__') and .//p[text()='{name}']]")
    #INGREDIENT_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal_opened__')]")
    CLOSE_MODAL_INGREDIENT = (By.XPATH, "//button[contains(@class, 'Modal_close__')]")


    # Локатор заголовка модального окна оформления заказа (содержит номер заказа)
    ORDER_MODAL_TITLE = (
        By.XPATH,
        "//h2[contains(@class, 'Modal_modal__title__2L34m')]"
    )

    @staticmethod
    def bun_image_by_name(name: str):
        return (
            By.XPATH,
            f"//img[@alt='{name}' and contains(@class,'BurgerIngredient_ingredient__image')]"
        )

    @staticmethod
    def sauce_image_by_name(name: str):
        return (
            By.XPATH,
            f"//img[@alt='{name}' and contains(@class,'BurgerIngredient_ingredient__image')]"
        )

    @staticmethod
    def filling_image_by_name(name: str):
        return (
            By.XPATH,
            f"//img[@alt='{name}' and contains(@class,'BurgerIngredient_ingredient__image')]"
        )

    @staticmethod
    def ingredient_item_by_name(name: str):
        return (
            By.XPATH,
            f"//p[text()='{name}']/ancestor::div[contains(@class,'BurgerIngredient_ingredient__wrapper')]"
        )

    @staticmethod
    def constructor_element_with_name(name: str):
        return (
            By.XPATH,
            f"//div[contains(@class,'constructor-element')]"
            f"//span[contains(@class,'constructor-element__text') and contains(text(),'{name}')]"
        )

    @staticmethod
    def ingredient_counter_by_name(name: str):
        return (
            By.XPATH,
            f"//p[text()='{name}']/ancestor::div[contains(@class,'BurgerIngredient_ingredient__')]"
            "//p[contains(@class,'counter_counter__num')]"
        )

    FIRST_INGREDIENT = (By.XPATH, "(//div[contains(@class, 'BurgerIngredient_ingredient__')])[1]")
    INGREDIENT_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal') and .//h2[contains(text(), 'Детали ингредиента')]]")
    MODAL_TITLE = (By.XPATH, "//h2[text()='Детали ингредиента']")

    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[.//*[local-name()='svg' and @width='24' and @height='24']]")
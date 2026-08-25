from selenium.webdriver.common.by import By


class MainPageLocators:
    PAGE_TITLE = (
        By.XPATH,
        "//h1[normalize-space()='Соберите бургер']",
    )

    FIRST_INGREDIENT = (
        By.CSS_SELECTOR,
        "a[class*='BurgerIngredient_ingredient']",
    )

    INGREDIENT_MODAL_TITLE = (
        By.XPATH,
        "//h2[normalize-space()='Детали ингредиента']",
    )

    INGREDIENT_MODAL = (
        By.CSS_SELECTOR,
        "div[class*='Modal_modal__contentBox']",
    )

    INGREDIENT_MODAL_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "button[class*='Modal_modal__close']",
    )

    FIRST_INGREDIENT_COUNTER = (
        By.CSS_SELECTOR,
        "a[class*='BurgerIngredient_ingredient'] [class*='counter_counter__num']",
    )

    CONSTRUCTOR_DROP_AREA = (
        By.CSS_SELECTOR,
        "section[class*='BurgerConstructor_basket']",
    )

    ORDER_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Оформить заказ']",
    )

    ORDER_MODAL = (
        By.XPATH,
        "//p[normalize-space()='Ваш заказ начали готовить']",
    )

    ORDER_MODAL_CLOSE_BUTTON = (
        By.CSS_SELECTOR,
        "button[class*='Modal_modal__close']",
    )

    ORDER_NUMBER = (
        By.CSS_SELECTOR,
        "h2.text_type_digits-large",
    )

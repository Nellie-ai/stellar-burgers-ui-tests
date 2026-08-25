from selenium.webdriver.common.by import By


class HeaderLocators:
    CONSTRUCTOR_LINK = (
        By.XPATH,
        "//header//a[@href='/' and .//*[normalize-space()='Конструктор']]",
    )

    ORDER_FEED_LINK = (
        By.XPATH,
        "//header//a[@href='/feed' and .//*[normalize-space()='Лента Заказов']]",
    )

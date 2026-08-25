from selenium.webdriver.common.by import By


class FeedPageLocators:
    PAGE_TITLE = (
        By.XPATH,
        "//h1[normalize-space()='Лента заказов']",
    )

    ORDER_CARDS = (
        By.CSS_SELECTOR,
        "a[href^='/feed/']",
    )

    TOTAL_ORDERS = (
        By.XPATH,
        "//p[normalize-space()='Выполнено за все время:']/following-sibling::p",
    )

    TODAY_ORDERS = (
        By.XPATH,
        "//p[normalize-space()='Выполнено за сегодня:']/following-sibling::p",
    )

    IN_PROGRESS_SECTION = (
        By.CSS_SELECTOR,
        "ul[class*='OrderFeed_orderListReady']",
    )

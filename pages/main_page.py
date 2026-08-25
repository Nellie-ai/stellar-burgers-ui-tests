import re

import allure
from selenium.common.exceptions import TimeoutException

from locators.header_locators import HeaderLocators
from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage
from utils.constants import BASE_URL, ORDER_TIMEOUT


class MainPage(BasePage):
    @allure.step("Дождаться авторизации пользователя")
    def wait_until_authorized(self):
        self.visible(MainPageLocators.ORDER_BUTTON)

    @allure.step("Открыть конструктор")
    def open_constructor(self):
        self.open(f"{BASE_URL}/")
        self.visible(MainPageLocators.PAGE_TITLE)

    @allure.step("Перейти в конструктор")
    def go_to_constructor(self):
        self.click(HeaderLocators.CONSTRUCTOR_LINK)
        self.wait_for_exact_url(f"{BASE_URL}/")

    @allure.step("Проверить, что открыт конструктор")
    def constructor_is_opened(self):
        if not self.current_url_is(f"{BASE_URL}/"):
            return False

        self.visible(MainPageLocators.PAGE_TITLE)
        return True

    @allure.step("Перейти в ленту заказов")
    def go_to_order_feed(self):
        self.click(HeaderLocators.ORDER_FEED_LINK)
        self.wait_for_exact_url(f"{BASE_URL}/feed")

    @allure.step("Открыть детали ингредиента")
    def open_ingredient_details(self):
        self.click(MainPageLocators.FIRST_INGREDIENT)
        self.visible(MainPageLocators.INGREDIENT_MODAL_TITLE)

    @allure.step("Проверить ингредиент в модальном окне")
    def modal_contains_ingredient(self, ingredient_name):
        if not self.is_visible(MainPageLocators.INGREDIENT_MODAL_TITLE):
            return False

        return ingredient_name in self.text(MainPageLocators.INGREDIENT_MODAL)

    @allure.step("Закрыть детали ингредиента")
    def close_ingredient_details(self):
        self.click(MainPageLocators.INGREDIENT_MODAL_CLOSE_BUTTON)
        self.wait_until_hidden(MainPageLocators.INGREDIENT_MODAL)

    @allure.step("Проверить закрытие деталей ингредиента")
    def ingredient_details_are_closed(self):
        return not self.is_visible(MainPageLocators.INGREDIENT_MODAL)

    @allure.step("Получить счётчик первого ингредиента")
    def ingredient_counter(self):
        try:
            text = self.text(
                MainPageLocators.FIRST_INGREDIENT_COUNTER,
                timeout=1,
            )
        except TimeoutException:
            return 0

        digits = re.sub(r"\D", "", text)
        return int(digits) if digits else 0

    @allure.step("Добавить ингредиент в конструктор")
    def add_ingredient(self):
        before = self.ingredient_counter()
        source = self.present(MainPageLocators.FIRST_INGREDIENT)
        target = self.present(MainPageLocators.CONSTRUCTOR_DROP_AREA)

        self.drag_and_drop(source, target)

        return self.wait_for_condition(
            lambda: self._increased_ingredient_counter(before),
            timeout=10,
        )

    def _increased_ingredient_counter(self, old_value):
        current = self.ingredient_counter()
        return current if current > old_value else False

    def _visible_order_number(self):
        for text in self.visible_texts(MainPageLocators.ORDER_NUMBER):
            number = re.sub(r"\D", "", text)

            if number:
                return number

        return False

    def _real_order_number(self):
        number = self._visible_order_number()
        return number if number and number != "9999" else False

    @allure.step("Создать заказ")
    def create_order(self):
        self.add_ingredient()
        self.click(MainPageLocators.ORDER_BUTTON)
        self.visible(MainPageLocators.ORDER_MODAL)

        return self.wait_for_condition(
            self._real_order_number,
            timeout=ORDER_TIMEOUT,
            poll_frequency=1,
        )

    @allure.step("Закрыть модальное окно заказа")
    def close_order_modal(self):
        self.click(MainPageLocators.ORDER_MODAL_CLOSE_BUTTON)
        self.wait_until_hidden(MainPageLocators.ORDER_MODAL)

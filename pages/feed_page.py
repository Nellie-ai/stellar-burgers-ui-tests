import re

import allure

from locators.feed_page_locators import FeedPageLocators
from pages.base_page import BasePage
from utils.constants import BASE_URL, ORDER_TIMEOUT


class FeedPage(BasePage):
    @allure.step("Открыть ленту заказов")
    def open_feed(self):
        self.open(f"{BASE_URL}/feed")
        self.visible(FeedPageLocators.PAGE_TITLE)

    @allure.step("Проверить, что открыта лента заказов")
    def feed_is_opened(self):
        if not self.current_url_is(f"{BASE_URL}/feed"):
            return False

        self.visible(FeedPageLocators.PAGE_TITLE)
        return True

    @allure.step("Получить количество заказов за всё время")
    def total_orders(self):
        return self._counter_value(FeedPageLocators.TOTAL_ORDERS)

    @allure.step("Получить количество заказов за сегодня")
    def today_orders(self):
        return self._counter_value(FeedPageLocators.TODAY_ORDERS)

    def _counter_value(self, locator):
        digits = re.sub(r"\D", "", self.text(locator))
        return int(digits) if digits else 0

    @staticmethod
    def _normalize_order_number(value):
        digits = re.sub(r"\D", "", str(value))

        if not digits:
            return ""

        return digits.lstrip("0") or "0"

    def _increased_counter(self, locator, old_value):
        current = self._counter_value(locator)
        return current if current > old_value else False

    @allure.step("Дождаться увеличения количества заказов за всё время")
    def wait_for_total_orders_increase(self, old_value):
        return self.wait_for_condition(
            lambda: self._increased_counter(
                FeedPageLocators.TOTAL_ORDERS,
                old_value,
            ),
            timeout=ORDER_TIMEOUT,
            poll_frequency=1,
        )

    @allure.step("Дождаться увеличения количества заказов за сегодня")
    def wait_for_today_orders_increase(self, old_value):
        return self.wait_for_condition(
            lambda: self._increased_counter(
                FeedPageLocators.TODAY_ORDERS,
                old_value,
            ),
            timeout=ORDER_TIMEOUT,
            poll_frequency=1,
        )

    def _order_is_in_progress(self, order_number):
        section_text = self.text(FeedPageLocators.IN_PROGRESS_SECTION)
        found_numbers = re.findall(r"\d+", section_text)
        normalized_numbers = {
            self._normalize_order_number(number) for number in found_numbers
        }

        return self._normalize_order_number(order_number) in normalized_numbers

    @allure.step("Дождаться появления заказа в работе")
    def wait_for_order_in_progress(self, order_number):
        return self.wait_for_condition(
            lambda: self._order_is_in_progress(order_number),
            timeout=ORDER_TIMEOUT,
            poll_frequency=1,
        )

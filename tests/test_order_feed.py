import allure

from pages.feed_page import FeedPage
from pages.main_page import MainPage


@allure.epic("Stellar Burgers")
@allure.feature("Лента заказов")
class TestOrderFeed:
    @allure.title("После создания заказа увеличивается «Выполнено за всё время»")
    def test_total_orders_increases_after_order(self, authorized_driver):
        feed_page = FeedPage(authorized_driver)
        feed_page.open_feed()
        before = feed_page.total_orders()

        main_page = MainPage(authorized_driver)
        main_page.go_to_constructor()
        main_page.create_order()
        main_page.close_order_modal()
        main_page.go_to_order_feed()

        after = feed_page.wait_for_total_orders_increase(before)

        assert after > before

    @allure.title("После создания заказа увеличивается «Выполнено за сегодня»")
    def test_today_orders_increases_after_order(self, authorized_driver):
        feed_page = FeedPage(authorized_driver)
        feed_page.open_feed()
        before = feed_page.today_orders()

        main_page = MainPage(authorized_driver)
        main_page.go_to_constructor()
        main_page.create_order()
        main_page.close_order_modal()
        main_page.go_to_order_feed()

        after = feed_page.wait_for_today_orders_increase(before)

        assert after > before

    @allure.title("Номер нового заказа появляется в секции «В работе»")
    def test_new_order_appears_in_progress(self, authorized_driver):
        main_page = MainPage(authorized_driver)
        main_page.open_constructor()

        order_number = main_page.create_order()
        main_page.close_order_modal()
        main_page.go_to_order_feed()

        order_is_visible = FeedPage(authorized_driver).wait_for_order_in_progress(
            order_number
        )

        assert order_is_visible

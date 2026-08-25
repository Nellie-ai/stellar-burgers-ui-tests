import allure

from pages.feed_page import FeedPage
from pages.main_page import MainPage
from utils.data import DEFAULT_INGREDIENT


@allure.epic("Stellar Burgers")
@allure.feature("Конструктор")
class TestConstructor:
    @allure.title("Переход в конструктор по клику на «Конструктор»")
    def test_click_constructor_opens_constructor(self, driver):
        feed_page = FeedPage(driver)
        feed_page.open_feed()
        main_page = MainPage(driver)

        main_page.go_to_constructor()

        assert main_page.constructor_is_opened()

    @allure.title("Переход в «Ленту заказов»")
    def test_click_order_feed_opens_feed(self, driver):
        main_page = MainPage(driver)
        main_page.open_constructor()

        main_page.go_to_order_feed()

        assert FeedPage(driver).feed_is_opened()

    @allure.title("Открытие модального окна с деталями ингредиента")
    def test_click_ingredient_opens_details(self, driver):
        main_page = MainPage(driver)
        main_page.open_constructor()

        main_page.open_ingredient_details()

        assert main_page.modal_contains_ingredient(DEFAULT_INGREDIENT)

    @allure.title("Закрытие модального окна с деталями крестиком")
    def test_close_button_closes_ingredient_details(self, driver):
        main_page = MainPage(driver)
        main_page.open_constructor()
        main_page.open_ingredient_details()

        main_page.close_ingredient_details()

        assert main_page.ingredient_details_are_closed()

    @allure.title("Счётчик ингредиента увеличивается после добавления")
    def test_ingredient_counter_increases_after_add(self, driver):
        main_page = MainPage(driver)
        main_page.open_constructor()
        before = main_page.ingredient_counter()

        after = main_page.add_ingredient()

        assert after == before + 2

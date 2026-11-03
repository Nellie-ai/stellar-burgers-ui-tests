"""Offline regressions for false positives; no browser or stand is used."""
from unittest.mock import Mock, patch

import pytest

from locators.feed_page_locators import FeedPageLocators
from pages.feed_page import FeedPage
from tests.test_order_feed import TestOrderFeed as OrderFeedScenarios


@pytest.mark.parametrize("section_text, expected", [
    ("001234\n001235", True),
    ("0012345\n001236", False),
    ("Все текущие заказы готовы!", False),
])
def test_order_membership_uses_exact_number(section_text, expected):
    page = FeedPage(Mock())
    page.text = Mock(return_value=section_text)
    assert page._section_contains_order(
        FeedPageLocators.COMPLETED_SECTION, "01234"
    ) is expected


@pytest.mark.parametrize("scenario", [
    "test_total_orders_increases_after_order",
    "test_today_orders_increases_after_order",
])
def test_foreign_counter_increase_cannot_replace_own_completed_order(scenario):
    with patch("tests.test_order_feed.MainPage") as main_cls, patch(
        "tests.test_order_feed.FeedPage"
    ) as feed_cls:
        main_cls.return_value.create_order.return_value = "1234"
        feed = feed_cls.return_value
        feed.total_orders.return_value = 100
        feed.today_orders.return_value = 100
        feed.wait_for_total_orders_increase.return_value = 101
        feed.wait_for_today_orders_increase.return_value = 101
        feed.wait_for_order_completed.return_value = False

        with pytest.raises(AssertionError):
            getattr(OrderFeedScenarios(), scenario)(Mock())
        feed.wait_for_order_completed.assert_called_once_with("1234")

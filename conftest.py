import allure
import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.base_page import BasePage
from pages.main_page import MainPage
from utils.api_client import StellarBurgersApi
from utils.constants import BASE_URL
from utils.data import generate_user


@pytest.fixture(
    params=[
        pytest.param("chrome", marks=pytest.mark.chrome),
        pytest.param("firefox", marks=pytest.mark.firefox),
    ]
)
def driver(request):
    browser = request.param

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,900")
        browser_driver = webdriver.Chrome(options=options)
    else:
        options = FirefoxOptions()
        options.add_argument("-headless")
        options.add_argument("--width=1280")
        options.add_argument("--height=900")
        browser_driver = webdriver.Firefox(options=options)

    try:
        BasePage(browser_driver).open(f"{BASE_URL}/")
        yield browser_driver
    finally:
        browser_driver.quit()


@pytest.fixture
def authorized_driver(driver):
    api = StellarBurgersApi()
    user = api.create_user(generate_user())
    page = BasePage(driver)

    try:
        page.set_local_storage("accessToken", user.access_token)
        page.set_local_storage("refreshToken", user.refresh_token)
        page.refresh()
        page.wait_for_exact_url(f"{BASE_URL}/")
        MainPage(driver).wait_until_authorized()
        yield driver
    finally:
        api.delete_user(user.access_token)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if not report.failed or report.when not in {"setup", "call"}:
        return

    driver = getattr(item, "funcargs", {}).get("driver")

    if driver is None:
        return

    try:
        allure.attach(
            BasePage(driver).screenshot_as_png(),
            name=f"failure_screenshot_{report.when}",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as error:
        item.add_report_section(
            report.when,
            "screenshot",
            f"Failed to capture screenshot: {error}",
        )

import allure

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
)
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def _wait(self, timeout=None, poll_frequency=0.5):
        return WebDriverWait(
            self.driver,
            timeout or self.timeout,
            poll_frequency=poll_frequency,
        )

    def wait_for_condition(
        self,
        condition,
        timeout=None,
        poll_frequency=0.5,
    ):
        return self._wait(timeout, poll_frequency).until(lambda _: condition())

    @allure.step("Открыть страницу")
    def open(self, url):
        self.driver.get(url)

    def refresh(self):
        self.driver.refresh()

    def visible(self, locator, timeout=None):
        return self._wait(timeout).until(EC.visibility_of_element_located(locator))

    def present(self, locator, timeout=None):
        return self._wait(timeout).until(EC.presence_of_element_located(locator))

    def clickable(self, locator, timeout=None):
        return self._wait(timeout).until(EC.element_to_be_clickable(locator))

    def all_present(self, locator, timeout=None):
        return self._wait(timeout).until(EC.presence_of_all_elements_located(locator))

    @allure.step("Кликнуть по элементу")
    def click(self, locator):
        element = self.clickable(locator)

        try:
            element.click()
        except ElementClickInterceptedException:
            self.driver.execute_script(
                "arguments[0].click();",
                element,
            )

    def text(self, locator, timeout=None):
        return self.visible(locator, timeout).text.strip()

    def visible_texts(self, locator):
        return [
            element.text.strip()
            for element in self.all_present(locator)
            if element.is_displayed()
        ]

    def is_visible(self, locator, timeout=2):
        try:
            self.visible(locator, timeout)
            return True
        except TimeoutException:
            return False

    def wait_until_hidden(self, locator, timeout=5):
        self._wait(timeout).until(EC.invisibility_of_element_located(locator))

    def wait_for_exact_url(self, url, timeout=10):
        self._wait(timeout).until(EC.url_to_be(url))

    def current_url_is(self, url):
        return self.driver.current_url.rstrip("/") == url.rstrip("/")

    def set_local_storage(self, key, value):
        self.driver.execute_script(
            "window.localStorage.setItem(arguments[0], arguments[1]);",
            key,
            value,
        )

    def screenshot_as_png(self):
        return self.driver.get_screenshot_as_png()

    def scroll_to(self, element):
        self.driver.execute_script(
            """
            arguments[0].scrollIntoView({
                block: 'center',
                inline: 'center'
            });
            """,
            element,
        )

    @allure.step("Перетащить элемент")
    def drag_and_drop(self, source, target):
        browser_name = self.driver.capabilities.get("browserName", "").lower()

        self.scroll_to(source)

        if browser_name == "firefox":
            self.driver.execute_script(
                """
                const source = arguments[0];
                const target = arguments[1];
                const dataTransfer = new DataTransfer();

                dataTransfer.effectAllowed = 'move';
                dataTransfer.dropEffect = 'move';
                dataTransfer.setData('text/plain', 'ingredient');

                function fireDragEvent(element, eventName, x, y) {
                    const event = new DragEvent(eventName, {
                        bubbles: true,
                        cancelable: true,
                        dataTransfer: dataTransfer,
                        clientX: x,
                        clientY: y
                    });

                    element.dispatchEvent(event);
                }

                const sourceRect = source.getBoundingClientRect();
                const targetRect = target.getBoundingClientRect();
                const sourceX = sourceRect.left + sourceRect.width / 2;
                const sourceY = sourceRect.top + sourceRect.height / 2;
                const targetX = targetRect.left + targetRect.width / 2;
                const targetY = targetRect.top + targetRect.height / 2;

                fireDragEvent(source, 'dragstart', sourceX, sourceY);
                fireDragEvent(target, 'dragenter', targetX, targetY);
                fireDragEvent(target, 'dragover', targetX, targetY);
                fireDragEvent(target, 'drop', targetX, targetY);
                fireDragEvent(source, 'dragend', targetX, targetY);
                """,
                source,
                target,
            )
        else:
            (
                ActionChains(self.driver)
                .move_to_element(source)
                .pause(0.3)
                .click_and_hold(source)
                .pause(0.3)
                .move_to_element(target)
                .pause(0.5)
                .release()
                .perform()
            )

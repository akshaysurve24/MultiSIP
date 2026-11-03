import os
import time
from pathlib import Path
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError


class BasePage:
    """
    Core Playwright wrapper providing standardized browser interactions,
    native & JS click fallbacks, character-by-character slow typing,
    and automatic full-page unblurred screenshots organized by Page Object class.
    """

    def __init__(self, page: Page):
        self.page = page

    def go_to(self, url: str):
        """Navigates to the specified URL and captures a navigation screenshot."""
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")
        self.take_screenshot("navigation")

    def click(self, locator: str, name_for_screenshot: str = "click", force: bool = False):
        """Standard Playwright click with auto-scroll and screenshot capture."""
        self.page.locator(locator).first.click(force=force)
        self.take_screenshot(name_for_screenshot)

    def js_click(self, locator: str, name_for_screenshot: str = "js_click"):
        """
        Bypasses transparent loading overlays, backdrop drawers, and sticky headers
        by invoking a direct JavaScript `.click()` evaluation on the DOM element.
        """
        self.page.locator(locator).first.evaluate("node => node.click()")
        self.take_screenshot(name_for_screenshot)

    def slow_fill(
        self,
        locator: str,
        text: str,
        delay_ms: float = 100,
        name_for_screenshot: str = "fill",
    ):
        """Fills an input field character-by-character with visual delay."""
        loc: Locator = self.page.locator(locator).first
        loc.clear()
        for char in str(text):
            loc.type(char, delay=delay_ms)
        self.take_screenshot(name_for_screenshot)

    def fill(self, locator: str, text: str, name_for_screenshot: str = "fill"):
        """Direct fill method for fast value entry followed by screenshot."""
        self.page.locator(locator).first.fill(str(text))
        self.take_screenshot(name_for_screenshot)

    def select_option_by_label(
        self, locator: str, label: str, name_for_screenshot: str = "select"
    ):
        """Selects an option from a <select> dropdown by its visible label string."""
        self.page.locator(locator).first.select_option(label=label)
        self.take_screenshot(name_for_screenshot)

    def select_option_by_value(
        self, locator: str, value: str, name_for_screenshot: str = "select"
    ):
        """Selects an option from a <select> dropdown by its value attribute."""
        self.page.locator(locator).first.select_option(value=value)
        self.take_screenshot(name_for_screenshot)

    def wait_for_selector(self, locator: str, state: str = "visible", timeout: float = 30000):
        """Waits for an element to match the specified state (visible, hidden, attached)."""
        self.page.wait_for_selector(locator, state=state, timeout=timeout)

    def wait(self, ms: int):
        """Explicit timeout wait in milliseconds."""
        self.page.wait_for_timeout(ms)

    def is_visible(self, locator: str, timeout: float = 5000) -> bool:
        """Checks if a selector is currently visible within the timeout window without failing."""
        try:
            self.page.wait_for_selector(locator, state="visible", timeout=timeout)
            return True
        except PlaywrightTimeoutError:
            return False

    def wait_for_url_contains(self, text: str, timeout: float = 30000):
        """Waits until the current page URL contains the specified substring."""
        self.page.wait_for_url(lambda url: text in url, timeout=timeout)

    def take_screenshot(self, name: str) -> str:
        """
        Captures full-page unblurred screenshots with CSS animations disabled.
        Automatically organizes files into a directory named after the calling Page Object class:
        screenshots/<PageObjectClassName>/<name>_<timestamp>.png
        """
        page_name = self.__class__.__name__
        # Locate project root screenshots directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        screenshot_dir = os.path.join(base_dir, "screenshots", page_name)
        os.makedirs(screenshot_dir, exist_ok=True)

        timestamp = int(time.time() * 1000)
        screenshot_path = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
        self.page.screenshot(
            path=screenshot_path,
            full_page=True,
            animations="disabled",
        )
        print(f"Screenshot saved to: {screenshot_path}")
        return screenshot_path


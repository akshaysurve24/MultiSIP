from pages.base_page import BasePage
from data.urls import AppURLs


class MultiSipLandingPage(BasePage):
    """
    Multi-SIP Landing Page Object.
    Handles 'Invest now' trigger and selecting the 'Do it yourself' (DIY) path.
    """

    def __init__(self, page):
        super().__init__(page)
        self.invest_now_button = "button:has-text('Invest now') >> visible=true"
        self.do_it_yourself_card = "h2:has-text('Do it yourself') >> visible=true"
        self.diy_container = "div:has(h2:has-text('Do it yourself')) >> visible=true"

    def navigate_to_multisip(self):
        """Directly navigates to the Multi-SIP landing page if required."""
        self.go_to(AppURLs.MULTISIP_URL)
        self.wait_for_selector(self.invest_now_button, state="visible")

    def click_invest_now(self):
        """Clicks the 'Invest now' primary button."""
        self.wait_for_selector(self.invest_now_button, state="visible", timeout=15000)
        self.click(self.invest_now_button, "click_invest_now_multisip")
        self.wait(1000)

    def select_do_it_yourself(self):
        """Selects the 'Do it yourself' journey card."""
        if self.is_visible(self.do_it_yourself_card, timeout=10000):
            self.click(self.do_it_yourself_card, "select_do_it_yourself")
        else:
            self.click(self.diy_container, "select_do_it_yourself_container")

        self.wait_for_url_contains("/multi-sip/diy", timeout=15000)
        self.wait(1000)


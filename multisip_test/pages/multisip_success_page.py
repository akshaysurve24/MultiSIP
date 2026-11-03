from pages.base_page import BasePage
from data.urls import AppURLs


class MultiSipSuccessPage(BasePage):
    """
    Multi-SIP Success Confirmation Page Object.
    Handles order verification, clicking 'Track Status', and 'Back to Home'.
    """

    def __init__(self, page):
        super().__init__(page)
        self.track_status_button = "button[aria-label='Track Status']"
        self.track_status_fallback = "button:has-text('Track Status') >> visible=true"
        self.back_to_home_button = "button[aria-label='Back to Home']"
        self.back_to_home_fallback = "button:has-text('Back to Home') >> visible=true"

    def click_track_status(self):
        """Clicks on the 'Track Status' button."""
        print("Clicking Track Status...")
        self.wait_for_selector(self.track_status_button, state="visible", timeout=15000)
        if self.is_visible(self.track_status_button, timeout=5000):
            self.click(self.track_status_button, "click_track_status")
        else:
            self.click(self.track_status_fallback, "click_track_status_fallback")
        self.wait(1000)

    def click_back_to_home(self):
        """Clicks on the 'Back to Home' button to complete the journey."""
        print("Clicking Back to Home...")
        if self.is_visible(self.back_to_home_button, timeout=8000):
            self.click(self.back_to_home_button, "click_back_to_home")
        else:
            self.click(self.back_to_home_fallback, "click_back_to_home_fallback")
        self.wait(1500)


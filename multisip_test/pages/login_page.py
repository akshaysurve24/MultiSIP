import time
from pages.base_page import BasePage
from data.urls import AppURLs


class LoginPage(BasePage):
    """
    Reusable Page Object for Investor Login across multiple journeys.
    Handles PAN entry, Terms & Conditions consent, Continue trigger, and 4-digit OTP.
    """

    def __init__(self, page):
        super().__init__(page)
        self.pan_input = "#panNumber"
        self.terms_checkbox = "#agree"
        self.continue_button = "button[type='submit']:has-text('Continue with PAN')"
        self.otp_digit_1 = "input[aria-label='OTP digit 1']"
        self.otp_digit_2 = "input[aria-label='OTP digit 2']"
        self.otp_digit_3 = "input[aria-label='OTP digit 3']"
        self.otp_digit_4 = "input[aria-label='OTP digit 4']"

    def navigate_to_login(self, url: str = None):
        """Navigates to the investor login page."""
        target_url = url or AppURLs.LOGIN_URL
        self.go_to(target_url)
        self.wait_for_selector(self.pan_input, state="visible")

    def enter_pan(self, pan: str):
        """Types the PAN number into the input field."""
        self.slow_fill(self.pan_input, pan.upper(), delay_ms=80, name_for_screenshot="enter_pan")

    def accept_terms(self):
        """Ensures the Terms and Conditions checkbox is checked."""
        checkbox = self.page.locator(self.terms_checkbox)
        state = checkbox.get_attribute("data-state")
        if state != "checked":
            self.click(self.terms_checkbox, "accept_terms_checkbox")
        else:
            print("Terms checkbox is already checked.")

    def click_continue(self):
        """Waits for the Continue button to become enabled after PAN autoload and clicks it."""
        # Wait until button is enabled (disabled attribute removed)
        self.page.wait_for_selector(
            "button[type='submit']:has-text('Continue with PAN'):not([disabled])",
            state="visible",
            timeout=15000,
        )
        self.click(self.continue_button, "click_continue_with_pan")

    def enter_otp(self, otp: str = "1234"):
        """Fills the 4-digit OTP into separate input boxes."""
        digits = [char for char in str(otp).strip()]
        if len(digits) < 4:
            raise ValueError(f"OTP must be at least 4 digits. Received: {otp}")

        self.wait_for_selector(self.otp_digit_1, state="visible", timeout=15000)
        otp_locators = [
            self.otp_digit_1,
            self.otp_digit_2,
            self.otp_digit_3,
            self.otp_digit_4,
        ]

        for idx, locator in enumerate(otp_locators):
            loc = self.page.locator(locator).first
            loc.fill(digits[idx])
            self.wait(150)

        self.take_screenshot("entered_login_otp")
        # Allow transition / redirect after OTP entry
        self.wait(2000)

    def login_with_pan(self, pan: str, otp: str = "1234"):
        """Complete helper to perform the full login flow."""
        self.enter_pan(pan)
        self.accept_terms()
        self.click_continue()
        self.enter_otp(otp)


from pages.base_page import BasePage
from data.urls import AppURLs


class MultiSipPaymentPage(BasePage):
    """
    Multi-SIP Payment Preview Page Object.
    Handles Recurring / One-Time Mandate (ROTM) selection,
    Bank account selection, Mandate amount input, and Proceeding to Gateway.
    """

    def __init__(self, page):
        super().__init__(page)
        self.rotm_accordion = "button:has-text('One Time Mandate')"
        self.rotm_accordion_second = "button:has-text('New One-Time Mandate')"
        self.bank_item_hdfc = "button:has-text('HDFC Bank Ltd')"
        self.bank_item_fallback = "div:has-text('HDFC Bank Ltd') >> visible=true"
        self.mandate_amount_input = "input[inputmode='numeric'][maxlength='7']"
        self.proceed_button = "button[aria-label='Proceed to payment']"
        self.proceed_button_fallback = "button:has-text('Proceed') >> visible=true"

    def expand_one_time_mandate(self):
        """Clicks the One Time Mandate accordion to reveal bank options."""
        self.wait_for_selector(self.rotm_accordion, state="visible", timeout=15000)
        btn = self.page.locator(self.rotm_accordion).first
        state = btn.get_attribute("data-state")
        if state != "open":
            btn.click()
            self.take_screenshot("expand_rotm_accordion")
            self.wait(1000)

    def expand_new_one_time_mandate(self):
        """Clicks the New One-Time Mandate accordion to reveal bank options."""
        target_locator = (
            self.rotm_accordion_second
            if self.is_visible(self.rotm_accordion_second, timeout=5000)
            else self.rotm_accordion
        )
        self.wait_for_selector(target_locator, state="visible", timeout=15000)
        btn = self.page.locator(target_locator).first
        state = btn.get_attribute("data-state")
        if state != "open":
            btn.click()
            self.take_screenshot("expand_rotm_accordion_second")
            self.wait(1000)

    def select_bank(self, bank_name: str = "HDFC Bank Ltd"):
        """Selects the specified bank from the mandate dropdown list."""
        print(f"Selecting bank: {bank_name}")
        bank_locator = f"button:has-text('{bank_name}')"
        if self.is_visible(bank_locator, timeout=8000):
            self.click(bank_locator, f"select_{bank_name.replace(' ', '_')}")
        else:
            self.page.locator(f"text={bank_name}").first.click()
            self.take_screenshot(f"select_{bank_name.replace(' ', '_')}_fallback")
        self.wait(500)

    def enter_mandate_amount(self, amount: str = "70000"):
        """Enters the mandate authorization amount."""
        print(f"Entering mandate amount: {amount}")
        amt_field = self.page.locator(self.mandate_amount_input).first
        if amt_field.is_visible():
            amt_field.fill(str(amount))
            self.take_screenshot("enter_mandate_amount")
        else:
            print("Direct mandate amount locator not visible; using fallback numeric field.")
            self.page.locator("input[inputmode='numeric']").last.fill(str(amount))
            self.take_screenshot("enter_mandate_amount_fallback")
        self.wait(500)

    def click_proceed_to_payment(self):
        """Clicks the Proceed button to navigate to payment gateway/simulation."""
        if self.is_visible(self.proceed_button, timeout=8000):
            self.click(self.proceed_button, "click_proceed_to_payment")
        else:
            self.click(self.proceed_button_fallback, "click_proceed_to_payment_fallback")
        self.wait(2000)

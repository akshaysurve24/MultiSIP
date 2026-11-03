import time
from typing import List
from pages.base_page import BasePage
from data.urls import AppURLs
from utils.data_generator import calculate_t_plus_days


class MultiSipDiyPage(BasePage):
    """
    Page Object for Multi-SIP Do-It-Yourself (DIY) Configuration Page.
    Handles Fund selection, T+2 start date, Step-up configurations,
    Folio switching, and SIP initialization OTP confirmation.
    """

    def __init__(self, page):
        super().__init__(page)
        # Fund Selection Elements
        self.add_funds_trigger = "div:has-text('Add Funds'):has(svg) >> visible=true"
        self.add_funds_dashed_box = "div.border-dashed:has-text('Add Funds') >> visible=true"
        self.all_funds_tab = "button[role='radio']:has-text('All Funds')"
        self.all_funds_tab_fallback = "button:has-text('All Funds') >> visible=true"
        self.add_funds_confirm_button = "button:has-text('Add Funds(') >> visible=true"

        # Folio Toggle
        self.toggle_folio_button = "button[aria-label='Toggle folio list']"

        # Terms & Start SIP
        self.start_sip_button = "button:has-text('Start Multi-SIP')"

        # OTP Modal
        self.otp_digit_1 = "input[aria-label='OTP digit 1']"
        self.otp_digit_2 = "input[aria-label='OTP digit 2']"
        self.otp_digit_3 = "input[aria-label='OTP digit 3']"
        self.otp_digit_4 = "input[aria-label='OTP digit 4']"

    def click_add_funds(self):
        """Clicks on the 'Add Funds' dashed container to open fund selection."""
        add_btn = self.page.locator("div.border-dashed, div:has-text('Add Funds')").filter(has_text="Add Funds").first
        if add_btn.is_visible(timeout=5000):
            add_btn.click()
            self.take_screenshot("click_add_funds")
        else:
            self.page.get_by_text("Add Funds").first.click()
            self.take_screenshot("click_add_funds_by_text")
        self.wait(1500)

    def click_all_funds_tab(self):
        """Switches to the 'All Funds' tab."""
        tab = self.page.locator("button[role='radio']:has-text('All Funds'), button:has-text('All Funds')").first
        tab.wait_for(state="visible", timeout=12000)
        tab.click()
        self.take_screenshot("click_all_funds_tab")
        self.wait(1500)

    def select_fund_by_name(self, fund_name: str):
        """
        Locates the specific fund card by its <h2> title and clicks
        its corresponding '+' button ('Add to selection').
        """
        print(f"Selecting fund: {fund_name}")
        card = self.page.locator("div, li, tr, section").filter(
            has=self.page.locator(f"h2:has-text('{fund_name}')")
        ).first

        add_btn = card.locator("button[aria-label='Add to selection']").first
        try:
            add_btn.wait_for(state="visible", timeout=8000)
            add_btn.click()
            self.take_screenshot(f"add_fund_{fund_name.replace(' ', '_')}")
            self.wait(500)
        except Exception as e:
            print(f"Direct card button click failed ({e}). Trying XPath fallback...")
            xpath_locator = (
                f"xpath=(//h2[contains(text(), '{fund_name}')]"
                f"/ancestor::*[.//button[@aria-label='Add to selection']][1]"
                f"//button[@aria-label='Add to selection'])[1]"
            )
            self.page.locator(xpath_locator).first.click()
            self.take_screenshot(f"add_fund_{fund_name.replace(' ', '_')}_xpath")
            self.wait(500)

    def add_multiple_funds(self, fund_names: List[str]):
        """Iterates over a list of fund names and clicks each one's '+' button."""
        for fund in fund_names:
            self.select_fund_by_name(fund)
        self.take_screenshot("all_funds_selected")

    def confirm_add_funds(self):
        """Clicks the confirmation 'Add Funds(N)' button and waits for the page return."""
        btn = self.page.locator("button:has-text('Add Funds('), button:has-text('Add Funds')").first
        btn.wait_for(state="visible", timeout=12000)
        btn.click()
        self.take_screenshot("confirm_add_funds_button")
        # Wait for transition back to DIY configure stepper
        self.wait(2000)

    def set_sip_start_date(self, days: int = 6):
        """Calculates T+N (default T+6) date and enters it into the SIP start date field."""
        target_date_str = calculate_t_plus_days(days)
        print(f"Setting SIP start date to T+{days}: {target_date_str}")

        date_input = self.page.locator(
            "input[inputmode='numeric'][class*='rounded-base'], input[class*='pr-12']"
        ).first

        if date_input.is_visible():
            date_input.click()
            date_input.fill(target_date_str)
            self.take_screenshot("set_sip_start_date")
        else:
            print("SIP start date input field not found directly; attempting fallback click.")
            self.page.locator("input[type='text']").first.fill(target_date_str)
            self.take_screenshot("set_sip_start_date_fallback")
        self.wait(500)

    # Alias for backwards compatibility
    set_sip_start_date_t_plus_2 = set_sip_start_date

    def select_folio(self, target_folio: str = "1049282369"):
        """
        Expands the Folio dropdown accordion and selects the target folio number.
        """
        print(f"Expanding folio list and selecting folio: {target_folio}")
        toggle_btn = self.page.locator(self.toggle_folio_button).first
        if toggle_btn.is_visible():
            state = toggle_btn.get_attribute("data-state")
            if state != "open":
                toggle_btn.click()
                self.take_screenshot("expand_folio_accordion")
                self.wait(800)

        # Select the target folio item from the expanded list
        folio_item = self.page.locator(
            f"xpath=//*[contains(text(), '{target_folio}')]"
        ).first

        if folio_item.is_visible():
            folio_item.click()
            self.take_screenshot(f"selected_folio_{target_folio}")
            self.wait(800)
        else:
            print(f"Warning: Folio {target_folio} not explicitly visible, trying text click...")
            self.page.locator(f"text={target_folio}").first.click()
            self.take_screenshot(f"selected_folio_{target_folio}_fallback")
            self.wait(500)

    def accept_terms_and_conditions(self):
        """Accepts terms & conditions checkbox on the DIY page."""
        print("Accepting Terms & Conditions checkbox...")
        checkboxes = self.page.locator("button[role='checkbox']").all()
        if checkboxes:
            target = checkboxes[-1]
            target.scroll_into_view_if_needed()
            self.wait(300)
            state = target.get_attribute("data-state")
            aria_checked = target.get_attribute("aria-checked")
            if state != "checked" and aria_checked != "true":
                try:
                    target.click(force=True, timeout=3000)
                except Exception:
                    target.evaluate("node => node.click()")
                self.take_screenshot("accept_diy_terms_checkbox")
                self.wait(500)

                # If still unchecked, trigger direct JS click
                if target.get_attribute("data-state") != "checked" and target.get_attribute("aria-checked") != "true":
                    target.evaluate("node => node.click()")
                    self.wait(500)

    def click_start_sip(self):
        """Waits for the Start Multi-SIP button to be enabled and clicks it with JS fallback."""
        print("Locating Start Multi-SIP button...")
        btn = self.page.locator("button:has-text('Start Multi-SIP')").last
        btn.wait_for(state="visible", timeout=15000)
        btn.scroll_into_view_if_needed()
        self.wait(500)

        # Check if button is disabled, wait for it to become enabled
        try:
            self.page.wait_for_selector(
                "button:has-text('Start Multi-SIP'):not([disabled])",
                state="visible",
                timeout=6000,
            )
            print("Start Multi-SIP button is enabled.")
        except Exception:
            print("Notice: Start Multi-SIP might be waiting on terms checkbox. Re-verifying terms...")
            self.accept_terms_and_conditions()
            self.wait(500)

        print("Clicking Start Multi-SIP...")
        try:
            btn.click(timeout=5000)
        except Exception as e:
            print(f"Native click failed ({e}), executing force click...")
            try:
                btn.click(force=True, timeout=5000)
            except Exception as e2:
                print(f"Force click failed ({e2}), executing DOM JS click...")
                btn.evaluate("node => node.click()")

        self.take_screenshot("clicked_start_multi_sip")
        self.wait(1500)

        # If OTP modal did not open yet, execute JS click fallback
        if not self.is_visible("input[aria-label='OTP digit 1']", timeout=3000):
            print("OTP modal not visible yet; re-triggering via direct JS evaluation click...")
            btn.evaluate("node => node.click()")
            self.take_screenshot("clicked_start_multi_sip_js_fallback")
            self.wait(1500)

    def enter_otp(self, otp: str = "1234"):
        """Enters the 4-digit OTP in the modal popup."""
        digits = [d for d in str(otp).strip()]
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

        self.take_screenshot("entered_start_sip_otp")
        # Wait for modal processing and redirect to payment
        self.wait_for_url_contains("/multi-sip/payment", timeout=20000)
        self.wait(1000)


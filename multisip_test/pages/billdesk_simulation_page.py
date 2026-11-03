from pages.base_page import BasePage
from data.urls import AppURLs


class BilldeskSimulationPage(BasePage):
    """
    Page Object for BillDesk Gateway Simulation.
    Allows selecting transaction simulation status (Success / Failure) and Submitting.
    """

    def __init__(self, page):
        super().__init__(page)
        self.status_dropdown = "select#status, select[name='status']"
        self.submit_button = "input[type='submit'][value='Submit'], button:has-text('Submit')"

    def select_status(self, status: str = "Success"):
        """Selects the transaction outcome status from the dropdown."""
        print(f"Selecting BillDesk simulation status: {status}")
        self.wait_for_selector(self.status_dropdown, state="visible", timeout=20000)
        self.select_option_by_value(self.status_dropdown, status, name_for_screenshot="select_billdesk_status")
        self.wait(500)

    def submit_simulation(self):
        """Clicks the Submit button to finalize simulation and return to portal."""
        self.click(self.submit_button, "submit_billdesk_simulation")
        # Wait for redirect back to the investor portal success page
        self.wait_for_url_contains("/multi-sip/success", timeout=25000)
        self.wait(1500)


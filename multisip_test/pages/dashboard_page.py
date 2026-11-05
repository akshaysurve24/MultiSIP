from pages.base_page import BasePage
from data.urls import AppURLs


class DashboardPage(BasePage):
    """
    Dashboard Page Object.
    Handles dismissals of regulatory popups (Nominee modal),
    Transact menu expansion, and navigation to Multi-SIP.
    """

    def __init__(self, page):
        super().__init__(page)
        self.dismiss_nominee_button = "button:has-text(\"I don't want to add a nominee\")"
        self.transact_button = "button[aria-haspopup='dialog']:has-text('Transact')"
        self.transact_fallback = "button:has-text('Transact') >> visible=true"
        self.multi_sip_menu_item = "button[role='menuitem']:has-text('Multi SIP')"
        self.multi_sip_fallback = "button:has-text('Multi SIP') >> visible=true"

    #def dismiss_nominee_popup_if_present(self, timeout: float = 6000):
       # """quick close pop up->Dismisses the nominee regulatory popup if it appears on login.-> issue in taking screenshot"""
       # try:
         #   if self.is_visible(self.dismiss_nominee_button, timeout=timeout):
          #      print("Nominee regulatory modal detected. Dismissing...")
          #      self.click(self.dismiss_nominee_button, "dismiss_nominee_popup")
          #      self.wait(1000)
          #  else:
          #      print("No nominee popup detected.")
        #except Exception as e:
           # print(f"Notice: nominee popup check ended: {e}")

    def dismiss_nominee_popup_if_present(self, timeout: float = 6000):
        """slow close pop up-> Waits for nominee popup, takes screenshot while visible, then dismisses it."""
        try:
            # 1. Wait for the popup button to appear
            if self.is_visible(self.dismiss_nominee_button, timeout=timeout):
                print("Nominee regulatory modal detected.")
                
                # 2. Settle timer: gives UI time to complete entrance animation (1-2 seconds)
                self.wait(1500)
                
                # 3. Take screenshot BEFORE clicking (while popup is fully displayed)
                self.take_screenshot("nominee_popup_displayed")
                
                # 4. Click the dismiss button
                print("Dismissing nominee popup...")
                self.page.locator(self.dismiss_nominee_button).first.click()
                
                # 5. Brief wait to allow modal close animation to finish
                self.wait(1000)
                self.take_screenshot("nominee_popup_dismissed")
            else:
                print("No nominee popup detected.")
        except Exception as e:
            print(f"Notice: nominee popup check ended: {e}")

    def click_transact(self):
        """Clicks the Transact button to open the actions menu."""
        if self.is_visible(self.transact_button, timeout=8000):
            self.click(self.transact_button, "click_transact_button")
        else:
            self.click(self.transact_fallback, "click_transact_fallback")
        self.wait(500)

    def click_multi_sip(self):
        """Clicks the Multi SIP option inside the Transact menu."""
        if self.is_visible(self.multi_sip_menu_item, timeout=8000):
            self.click(self.multi_sip_menu_item, "click_multi_sip_menu")
        else:
            self.click(self.multi_sip_fallback, "click_multi_sip_fallback")

        # Wait for transition towards multi-sip page
        self.wait_for_url_contains("/multi-sip", timeout=15000)
        self.wait(1000)

    
    
     #optional full flow adding above all functions in below one fuction  and then  calling below function in test_multisip_flow.py to reduce code.
    def navigate_to_multisip(self):
       
        """
        Performs the complete dashboard flow:
        1. Dismiss nominee popup
        2. Click Transact
        3. Click Multi SIP
        """
        self.dismiss_nominee_popup_if_present(timeout=15000)
        self.click_transact()
        self.click_multi_sip()
        
        

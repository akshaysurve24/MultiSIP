import pytest
from playwright.sync_api import Page, expect
from data.urls import AppURLs
from data.test_data import TestData
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.multisip_landing_page import MultiSipLandingPage
from pages.multisip_diy_page import MultiSipDiyPage
from pages.multisip_payment_page import MultiSipPaymentPage
from pages.billdesk_simulation_page import BilldeskSimulationPage
from pages.multisip_success_page import MultiSipSuccessPage


def test_end_to_end_multisip_diy_journey(page: Page):
    """
    Master End-to-End Test for the Multi-SIP DIY Journey.
    Executes Login -> Dashboard -> Multi-SIP DIY Fund Selection ->
    T+6 Start Date -> Folio Selection -> Terms -> OTP ->
    ROTM Bank Mandate -> BillDesk Simulation -> Success Confirmation.
    """

    # 1. Initialize Page Objects
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)
    landing_page = MultiSipLandingPage(page)
    diy_page = MultiSipDiyPage(page)
    payment_page = MultiSipPaymentPage(page)
    billdesk_page = BilldeskSimulationPage(page)
    success_page = MultiSipSuccessPage(page)

    # -------------------------------------------------------------
    # Step 1-4: Reusable Investor Login
    # -------------------------------------------------------------
    print("=== Step 1: Navigating to Login Page ===")
    login_page.navigate_to_login(AppURLs.LOGIN_URL)

    print("=== Step 2: Entering PAN ===")
    login_page.enter_pan(TestData.PAN)

    print("=== Step 3: Accepting Terms & Conditions ===")
    login_page.accept_terms()

    print("=== Step 4: Submitting Continue and Entering OTP ===")
    login_page.click_continue()
    login_page.enter_otp(TestData.OTP)

    # -------------------------------------------------------------
    # Step 5-7: Dashboard Navigation to Multi-SIP
    # -------------------------------------------------------------
    print("=== Step 5: Handling Regulatory Nominee Popup ===")
    dashboard_page.dismiss_nominee_popup_if_present()

    print("=== Step 6: Opening Transact Menu ===")
    dashboard_page.click_transact()

    print("=== Step 7: Navigating to Multi-SIP ===")
    dashboard_page.click_multi_sip()
    assert "/multi-sip" in page.url, f"Expected '/multi-sip' in URL, got {page.url}"

    # -------------------------------------------------------------
    # Step 8-9: Multi-SIP Landing Page
    # -------------------------------------------------------------
    print("=== Step 8: Clicking Invest Now on Multi-SIP Landing ===")
    landing_page.click_invest_now()

    print("=== Step 9: Selecting Do It Yourself (DIY) Mode ===")
    landing_page.select_do_it_yourself()
    assert "/multi-sip/diy" in page.url, f"Expected '/multi-sip/diy' in URL, got {page.url}"

    # -------------------------------------------------------------
    # Step 10-13: Fund Selection (5 Selected Funds)
    # -------------------------------------------------------------
    print("=== Step 10: Opening Fund Explorer ===")
    diy_page.click_add_funds()

    print("=== Step 11: Switching to All Funds Tab ===")
    diy_page.click_all_funds_tab()

    print(f"=== Step 12: Adding {len(TestData.SELECTED_FUNDS)} Funds by Name ===")
    diy_page.add_multiple_funds(TestData.SELECTED_FUNDS)

    print("=== Step 13: Confirming Selected Funds ===")
    diy_page.confirm_add_funds()

    # -------------------------------------------------------------
    # Step 14-16: SIP Configuration (T+6 Date & Folio Selection)
    # -------------------------------------------------------------
    print(f"=== Step 14: Setting T+{TestData.SIP_START_DATE_DAYS} SIP Start Date ===")
    diy_page.set_sip_start_date(days=TestData.SIP_START_DATE_DAYS)

    print(f"=== Step 15: Selecting Folio Number {TestData.FOLIO_NUMBER} ===")
    diy_page.select_folio(TestData.FOLIO_NUMBER)

    print("=== Step 16: Accepting Terms & Submitting Start SIP ===")
    diy_page.accept_terms_and_conditions()
    diy_page.click_start_sip()

    print("=== Step 17: Entering OTP for SIP Authorization ===")
    diy_page.enter_otp(TestData.OTP)
    assert "/multi-sip/payment" in page.url, f"Expected '/multi-sip/payment' in URL, got {page.url}"

    # -------------------------------------------------------------
    # Step 18-20: ROTM Mandate & Bank Setup
    # -------------------------------------------------------------
    payment_page.expand_one_time_mandate()
    
    print("=== Step 18: Expanding New One-Time Mandate (ROTM) ===")
    payment_page.expand_new_one_time_mandate()

    print(f"=== Step 19: Selecting Bank Account: {TestData.MANDATE_BANK_NAME} ===")
    payment_page.select_bank(TestData.MANDATE_BANK_NAME)

    print(f"=== Step 20: Entering Mandate Amount: {TestData.MANDATE_AMOUNT} & Proceeding ===")
    payment_page.enter_mandate_amount(TestData.MANDATE_AMOUNT)
    payment_page.click_proceed_to_payment()

    # -------------------------------------------------------------
    # Step 21: BillDesk Gateway Simulation
    # -------------------------------------------------------------
    print(f"=== Step 21: Simulating Gateway Status: {TestData.BILLDESK_STATUS} ===")
    billdesk_page.select_status(TestData.BILLDESK_STATUS)
    billdesk_page.submit_simulation()

    # -------------------------------------------------------------
    # Step 22-24: Multi-SIP Success Confirmation
    # -------------------------------------------------------------
    print("=== Step 22: Verifying Success Confirmation Page ===")
    assert "/multi-sip/success" in page.url, f"Expected '/multi-sip/success' in URL, got {page.url}"

    print("=== Step 23: Clicking Track Status ===")
    success_page.click_track_status()

    print("=== Step 24: Clicking Back to Home ===")
    success_page.click_back_to_home()

    print("=== Multi-SIP DIY Journey Completed Successfully! ===")


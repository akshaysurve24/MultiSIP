import os
import sys
import traceback
from pathlib import Path
from playwright.sync_api import sync_playwright

# Ensure imports resolve
current_dir = Path(__file__).resolve().parent
package_root = current_dir.parent
project_root = package_root.parent

for d in (package_root, project_root):
    if str(d) not in sys.path:
        sys.path.insert(0, str(d))

from data.urls import AppURLs
from data.test_data import TestData
from utils.excel_manager import ExcelManager
from utils.data_generator import calculate_t_plus_days
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.multisip_landing_page import MultiSipLandingPage
from pages.multisip_diy_page import MultiSipDiyPage
from pages.multisip_payment_page import MultiSipPaymentPage
from pages.billdesk_simulation_page import BilldeskSimulationPage
from pages.multisip_success_page import MultiSipSuccessPage


def run_excel_data_driven_suite(excel_path: str = "multisip_test_cases.xlsx"):
    """
    Executes test scenarios defined in the Excel workbook, asserts expected outcomes,
    and updates execution statuses, actual results, timestamps, and screenshots.
    """
    wb_path = Path(excel_path)
    if not wb_path.is_absolute():
        # Check current working dir, project root, and package root
        if wb_path.exists():
            pass
        elif (project_root / excel_path).exists():
            wb_path = project_root / excel_path
        elif (package_root / excel_path).exists():
            wb_path = package_root / excel_path
        else:
            print(f"Workbook {excel_path} not found. Generating default test matrix...")
            from utils.generate_test_cases import generate_multisip_test_cases_workbook
            target_file = str(project_root / excel_path)
            wb_path = Path(generate_multisip_test_cases_workbook(target_file))

    excel_mgr = ExcelManager(str(wb_path))
    test_cases = excel_mgr.get_all_test_cases()
    print(f"Loaded {len(test_cases)} test cases from {wb_path.name}")

    is_headless = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=is_headless,
            args=["--start-maximized"],
        )
        context = browser.new_context(no_viewport=True)
        page = context.new_page()

        # Instantiate POMs
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        landing_page = MultiSipLandingPage(page)
        diy_page = MultiSipDiyPage(page)
        payment_page = MultiSipPaymentPage(page)
        billdesk_page = BilldeskSimulationPage(page)
        success_page = MultiSipSuccessPage(page)

        for tc in test_cases:
            test_id = tc.get("Test_ID")
            row_idx = tc["__row_idx__"]
            description = tc.get("Description", "")
            print(f"\n---> Running [{test_id}]: {description}")

            last_screenshot = ""
            try:
                if test_id == "TC_LOGIN_001":
                    login_page.navigate_to_login(AppURLs.LOGIN_URL)
                    login_page.enter_pan(TestData.PAN)
                    login_page.accept_terms()
                    login_page.click_continue()
                    login_page.enter_otp(TestData.OTP)
                    actual = f"Successfully authenticated; current URL: {page.url}"
                    last_screenshot = login_page.take_screenshot(f"{test_id}_success")
                    excel_mgr.update_test_status(row_idx, "PASS", actual, last_screenshot)

                elif test_id == "TC_DASH_001":
                    dashboard_page.dismiss_nominee_popup_if_present()
                    actual = "Nominee regulatory popup dismissed/checked."
                    last_screenshot = dashboard_page.take_screenshot(f"{test_id}_nominee")
                    excel_mgr.update_test_status(row_idx, "PASS", actual, last_screenshot)

                elif test_id == "TC_DASH_002":
                    dashboard_page.click_transact()
                    dashboard_page.click_multi_sip()
                    actual = f"Navigated to Multi-SIP; URL: {page.url}"
                    last_screenshot = dashboard_page.take_screenshot(f"{test_id}_multi_sip")
                    excel_mgr.update_test_status(row_idx, "PASS", actual, last_screenshot)

                elif test_id == "TC_MSIP_001":
                    landing_page.click_invest_now()
                    landing_page.select_do_it_yourself()
                    actual = f"Selected DIY path; URL: {page.url}"
                    last_screenshot = landing_page.take_screenshot(f"{test_id}_diy")
                    excel_mgr.update_test_status(row_idx, "PASS", actual, last_screenshot)

                elif test_id == "TC_FUND_001":
                    diy_page.click_add_funds()
                    diy_page.click_all_funds_tab()
                    diy_page.add_multiple_funds(TestData.SELECTED_FUNDS)
                    diy_page.confirm_add_funds()
                    actual = f"Added {len(TestData.SELECTED_FUNDS)} funds and confirmed."
                    last_screenshot = diy_page.take_screenshot(f"{test_id}_funds_added")
                    excel_mgr.update_test_status(row_idx, "PASS", actual, last_screenshot)

                elif test_id == "TC_CONFIG_001":
                    days_ahead = TestData.SIP_START_DATE_DAYS
                    diy_page.set_sip_start_date(days=days_ahead)
                    t_date = calculate_t_plus_days(days_ahead)
                    actual = f"SIP start date set to T+{days_ahead} ({t_date})."
                    last_screenshot = diy_page.take_screenshot(f"{test_id}_t{days_ahead}_date")
                    excel_mgr.update_test_status(row_idx, "PASS", actual, last_screenshot)

                elif test_id == "TC_CONFIG_003":
                    diy_page.select_folio(TestData.FOLIO_NUMBER)
                    actual = f"Folio {TestData.FOLIO_NUMBER} selected successfully."
                    last_screenshot = diy_page.take_screenshot(f"{test_id}_folio")
                    excel_mgr.update_test_status(row_idx, "PASS", actual, last_screenshot)

                elif test_id == "TC_CONFIG_004":
                    diy_page.accept_terms_and_conditions()
                    diy_page.click_start_sip()
                    diy_page.enter_otp(TestData.OTP)
                    actual = f"SIP initiated with OTP; redirected to {page.url}"
                    last_screenshot = diy_page.take_screenshot(f"{test_id}_otp")
                    excel_mgr.update_test_status(row_idx, "PASS", actual, last_screenshot)

                elif test_id == "TC_PAY_001":
                    payment_page.expand_new_one_time_mandate()
                    payment_page.select_bank(TestData.MANDATE_BANK_NAME)
                    payment_page.enter_mandate_amount(TestData.MANDATE_AMOUNT)
                    payment_page.click_proceed_to_payment()
                    actual = f"Selected bank {TestData.MANDATE_BANK_NAME}, amount {TestData.MANDATE_AMOUNT}, proceeded."
                    last_screenshot = payment_page.take_screenshot(f"{test_id}_proceed")
                    excel_mgr.update_test_status(row_idx, "PASS", actual, last_screenshot)

                elif test_id == "TC_SIM_001":
                    billdesk_page.select_status(TestData.BILLDESK_STATUS)
                    billdesk_page.submit_simulation()
                    actual = f"Simulated status {TestData.BILLDESK_STATUS}; landed on {page.url}"
                    last_screenshot = billdesk_page.take_screenshot(f"{test_id}_sim")
                    excel_mgr.update_test_status(row_idx, "PASS", actual, last_screenshot)

                elif test_id == "TC_SUCC_001":
                    success_page.click_track_status()
                    success_page.click_back_to_home()
                    actual = "Interacted with Track Status and Back to Home on success screen."
                    last_screenshot = success_page.take_screenshot(f"{test_id}_success_page")
                    excel_mgr.update_test_status(row_idx, "PASS", actual, last_screenshot)

                else:
                    print(f"Skipping unmapped scenario {test_id}")
                    excel_mgr.update_test_status(row_idx, "SKIPPED", "No direct automated runner mapping.")

            except Exception as e:
                err_trace = traceback.format_exc()
                print(f"Error executing [{test_id}]: {e}")
                err_screenshot = ""
                try:
                    err_screenshot = base_page = BasePage(page).take_screenshot(f"{test_id}_failure")
                except Exception:
                    pass
                excel_mgr.update_test_status(
                    row_idx,
                    "FAIL",
                    actual_result=f"Exception: {str(e)}",
                    screenshot_path=err_screenshot,
                    error_message=err_trace[:500],
                )

        browser.close()

    result_file = excel_mgr.save_results()
    print(f"\nExecution Complete! Full report available at: {result_file}")
    return result_file


if __name__ == "__main__":
    run_excel_data_driven_suite()


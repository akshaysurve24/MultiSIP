import os
import sys
from pathlib import Path
import openpyxl

# Ensure package directories resolve cleanly in sys.path
CURRENT_DIR = Path(__file__).resolve().parent
MULTISIP_TEST_DIR = CURRENT_DIR.parent
PROJECT_ROOT = MULTISIP_TEST_DIR.parent

for directory in (MULTISIP_TEST_DIR, PROJECT_ROOT):
    dir_str = str(directory)
    if dir_str not in sys.path:
        sys.path.insert(0, dir_str)

from utils.excel_utils import ExcelUtils


def generate_multisip_test_cases_workbook(output_path: str = "multisip_test_cases.xlsx") -> str:
    """
    Generates a structured Excel test-case workbook with Positive,
    Negative, and Boundary scenarios covering the Multi-SIP journey.
    """
    target_path = Path(output_path)
    if not target_path.is_absolute():
        target_path = PROJECT_ROOT / output_path

    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = "MultiSIP_Test_Cases"

    headers = [
        "Test_ID",
        "Module",
        "Scenario_Type",
        "Description",
        "Test_Steps",
        "Input_Data",
        "Expected_Result",
        "Actual_Result",
        "Status",
        "Execution_Timestamp",
        "Screenshot_Path",
        "Error_Details",
    ]
    sheet.append(headers)

    test_cases = [
        # --- LOGIN MODULE ---
        (
            "TC_LOGIN_001",
            "Login",
            "Positive",
            "Verify investor login with valid PAN and valid default OTP",
            "1. Navigate to login URL\n2. Enter valid PAN\n3. Check terms & conditions\n4. Click Continue\n5. Enter OTP 1234",
            "PAN: eyzps3598j, OTP: 1234",
            "User is authenticated and redirected to Dashboard",
            "",
            "Pending",
            "",
            "",
            "",
        ),
        (
            "TC_LOGIN_002",
            "Login",
            "Negative",
            "Verify login with invalid PAN format",
            "1. Navigate to login URL\n2. Enter malformed PAN\n3. Attempt to proceed",
            "PAN: INVALID123",
            "System displays PAN format validation error; Continue button disabled",
            "",
            "Pending",
            "",
            "",
            "",
        ),
        (
            "TC_LOGIN_003",
            "Login",
            "Negative",
            "Verify Continue button disabled when Terms & Conditions checkbox is unchecked",
            "1. Navigate to login URL\n2. Enter valid PAN\n3. Leave terms unchecked",
            "PAN: eyzps3598j, Terms: Unchecked",
            "Continue with PAN button remains disabled",
            "",
            "Pending",
            "",
            "",
            "",
        ),
        (
            "TC_LOGIN_004",
            "Login",
            "Negative",
            "Verify login rejection when incorrect OTP is entered",
            "1. Enter PAN and continue\n2. Enter incorrect OTP 9999",
            "OTP: 9999",
            "System displays invalid OTP error message",
            "",
            "Pending",
            "",
            "",
            "",
        ),

        # --- DASHBOARD & NAVIGATION ---
        (
            "TC_DASH_001",
            "Dashboard",
            "Positive",
            "Verify dismiss nominee regulatory popup if present",
            "1. Observe dashboard post-login\n2. Click 'I don't want to add a nominee'",
            "Action: Dismiss popup",
            "Nominee modal is closed and dashboard becomes interactive",
            "",
            "Pending",
            "",
            "",
            "",
        ),
        (
            "TC_DASH_002",
            "Dashboard",
            "Positive",
            "Verify opening Transact menu and navigating to Multi-SIP",
            "1. Click Transact button\n2. Click Multi SIP menu item",
            "Menu item: Multi SIP",
            "User is redirected to /multi-sip landing page",
            "",
            "Pending",
            "",
            "",
            "",
        ),

        # --- MULTI-SIP LANDING & SELECTION ---
        (
            "TC_MSIP_001",
            "MultiSIP_Landing",
            "Positive",
            "Verify clicking Invest Now and selecting Do It Yourself mode",
            "1. On /multi-sip click Invest now\n2. Select Do it yourself card",
            "Mode: Do it yourself",
            "User is redirected to /multi-sip/diy configuration page",
            "",
            "Pending",
            "",
            "",
            "",
        ),

        # --- FUND EXPLORER & SELECTION ---
        (
            "TC_FUND_001",
            "Fund_Selection",
            "Positive",
            "Verify adding 5 selected funds from All Funds tab",
            "1. Click Add Funds\n2. Switch to All Funds tab\n3. Add Gold, Infra, Smallcap, Midcap, Flexi Cap funds\n4. Click Add Funds(5)",
            "Funds: ABSL Gold, Infra, Smallcap, Midcap, Flexi Cap",
            "All 5 funds are added to SIP cart and configuration summary updates",
            "",
            "Pending",
            "",
            "",
            "",
        ),
        (
            "TC_FUND_002",
            "Fund_Selection",
            "Boundary",
            "Verify add funds confirmation button updates count dynamically",
            "1. Click '+' for multiple funds\n2. Verify label 'Add Funds(N)'",
            "N = 5",
            "Button text displays 'Add Funds(5)' and is enabled",
            "",
            "Pending",
            "",
            "",
            "",
        ),

        # --- SIP CONFIGURATION (T+6, STEP-UP, FOLIO) ---
        (
            "TC_CONFIG_001",
            "SIP_Config",
            "Positive",
            "Verify setting SIP start date using T+6 business date calculation",
            "1. Calculate T+6 date from current date\n2. Fill SIP start date input",
            "Date: T+6 (DD/MM/YYYY)",
            "SIP start date accepts valid T+6 date without validation error",
            "",
            "Pending",
            "",
            "",
            "",
        ),
        (
            "TC_CONFIG_003",
            "SIP_Config",
            "Positive",
            "Verify expanding folio accordion and selecting specific folio number",
            "1. Click Toggle folio list accordion\n2. Select folio 1049282369",
            "Folio: 1049282369",
            "Target folio is selected and displays as active folio",
            "",
            "Pending",
            "",
            "",
            "",
        ),
        (
            "TC_CONFIG_004",
            "SIP_Config",
            "Positive",
            "Verify accepting Terms and submitting Start SIP with OTP authorization",
            "1. Check terms checkbox\n2. Click Start SIP\n3. Enter OTP 1234",
            "Terms: Checked, OTP: 1234",
            "SIP configuration is authorized and user is redirected to payment preview",
            "",
            "Pending",
            "",
            "",
            "",
        ),

        # --- PAYMENT & MANDATE ---
        (
            "TC_PAY_001",
            "Payment",
            "Positive",
            "Verify selecting ROTM (New One-Time Mandate) and choosing bank account",
            "1. Expand New One-Time Mandate accordion\n2. Select HDFC Bank Ltd account\n3. Enter mandate amount 70000\n4. Click Proceed",
            "Bank: HDFC Bank Ltd, Amount: 70000",
            "Mandate is configured and user transitions to payment gateway simulation",
            "",
            "Pending",
            "",
            "",
            "",
        ),

        # --- GATEWAY SIMULATION & SUCCESS ---
        (
            "TC_SIM_001",
            "Gateway_Simulation",
            "Positive",
            "Verify simulating Success transaction on BillDesk simulator",
            "1. Select 'Success' from dropdown\n2. Click Submit button",
            "Status: Success",
            "Gateway processes transaction and redirects to /multi-sip/success page",
            "",
            "Pending",
            "",
            "",
            "",
        ),
        (
            "TC_SUCC_001",
            "Success_Page",
            "Positive",
            "Verify interacting with Track Status and Back to Home on success screen",
            "1. Click Track Status button\n2. Click Back to Home button",
            "Action: Post-transaction navigation",
            "Order status is tracked and user safely returns to home portal dashboard",
            "",
            "Pending",
            "",
            "",
            "",
        ),
    ]

    for tc in test_cases:
        sheet.append(tc)

    # Apply professional styling
    ExcelUtils.style_header_row(sheet, row_num=1)
    ExcelUtils.auto_fit_columns(sheet)

    wb.save(str(target_path))
    print(f"Generated Multi-SIP test cases matrix: {target_path}")
    return str(target_path)


if __name__ == "__main__":
    generate_multisip_test_cases_workbook("multisip_test_cases.xlsx")


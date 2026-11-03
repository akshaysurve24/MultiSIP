import os
from data.urls import AppURLs


class TestData:
    """
    Non-secret test constants and configurable parameters for Multi-SIP.
    Sensitive values (PAN, OTP, bank account) load from environment variables with safe test defaults.
    """

    # 1. Multi-SIP Journey Identity & Login
    PAN = os.getenv("TEST_PAN", "eyzps3598j")
    OTP = os.getenv("TEST_OTP", "1234")

    # 2. Target Funds for Multi-SIP DIY Journey
    SELECTED_FUNDS = [
        "ABSL Gold Fund",
        "ABSL Infrastructure Fund",
        "ABSL Smallcap Fund",
        "ABSL Midcap Fund",
        "ABSL Flexi Cap Fund",
    ]

    # 3. SIP Configuration Details
    SIP_START_DATE_DAYS = int(os.getenv("SIP_START_DATE_DAYS", "6"))  # T+6 business logic

    # 4. Folio Selection
    FOLIO_NUMBER = os.getenv("TEST_FOLIO", "1049282369")

    # 5. Mandate & Payment (ROTM)
    MANDATE_BANK_NAME = os.getenv("MANDATE_BANK", "HDFC Bank Ltd")
    MANDATE_AMOUNT = os.getenv("MANDATE_AMOUNT", "70000")
    BILLDESK_STATUS = "Success"

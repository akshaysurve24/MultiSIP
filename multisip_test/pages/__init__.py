"""Pages package exporting all POM classes for Multi-SIP."""
from pages.base_page import BasePage
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.multisip_landing_page import MultiSipLandingPage
from pages.multisip_diy_page import MultiSipDiyPage
from pages.multisip_payment_page import MultiSipPaymentPage
from pages.billdesk_simulation_page import BilldeskSimulationPage
from pages.multisip_success_page import MultiSipSuccessPage

__all__ = [
    "BasePage",
    "LoginPage",
    "DashboardPage",
    "MultiSipLandingPage",
    "MultiSipDiyPage",
    "MultiSipPaymentPage",
    "BilldeskSimulationPage",
    "MultiSipSuccessPage",
]

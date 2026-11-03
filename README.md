# Multi-SIP Automation Framework (Playwright + Python)

Enterprise-grade Page Object Model (POM) automation framework for the **Aditya Birla Sun Life Mutual Fund (ABSLMF) Multi-SIP Journey**.

---

## 🚀 Key Framework Features

- **Page Object Model (POM)**: Strict separation of locators and actions across dedicated screens (`LoginPage`, `DashboardPage`, `MultiSipLandingPage`, `MultiSipDiyPage`, `MultiSipPaymentPage`, `BilldeskSimulationPage`, `MultiSipSuccessPage`).
- **Single Centralized Configuration & Dependencies**: Merged single root [`conftest.py`](file:///d:/PW_Scripts/New_portal/MultiSIP/conftest.py) for all Pytest fixtures and viewport maximization, and single [`requirements.txt`](file:///d:/PW_Scripts/New_portal/MultiSIP/requirements.txt) at project root.
- **Centralized URL & Environment Routing**: All URLs, domains, and parameterized endpoints are managed centrally in `data/urls.py` (`LOCAL`, `QA`, `UAT`, `PROD`).
- **Desktop Window Maximization**: Solves viewport clipping and responsive hamburger menus via `no_viewport=True` and `--start-maximized` in `conftest.py`.
- **Dynamic Date Logic**: Built-in T+6 date calculator for SIP starting dates.
- **Traceable Full-Page Screenshots**: Captures complete DOM pages with CSS animations disabled, saved automatically under `screenshots/<PageObjectClassName>/`.
- **Data-Driven Excel Execution**: Scaffolds test matrices (`generate_test_cases.py`) and executes them via `run_excel_tests.py`, writing back PASS/FAIL results and execution timestamps.
- **Secret & Test Data Segregation**: Non-secret configurations in `data/test_data.py` with support for environment variables (`.env`).

---

## 📁 Project Structure

```text
MultiSIP/
├── .agents/
│   └── AGENTS.md                                # AI & Developer automation guidelines
├── .env.example                                 # Template for environment variables
├── requirements.txt                             # Consolidated project dependencies
├── conftest.py                                  # Consolidated Pytest fixtures & viewport config
├── command.txt                                  # Quick CLI execution cheat sheet
├── uat script.txt                               # Original UAT requirements specification
├── implementation_plans/                        # Framework architecture blueprints
│   ├── centralized_url_management_blueprint.md
│   ├── folderwise_screenshot_store.md
│   ├── full_page_screenshot_logic.md
│   ├── playwright_viewport_fix.md
│   └── end_to_end_project_implementation_plan_blueprint.md
└── multisip_test/
    ├── data/
    │   ├── __init__.py
    │   ├── urls.py                              # Central AppURLs
    │   └── test_data.py                         # TestData constants
    ├── pages/
    │   ├── base_page.py                         # Playwright wrapper with auto-screenshots
    │   ├── login_page.py                        # PAN, Terms, Continue, 4-digit OTP
    │   ├── dashboard_page.py                    # Nominee modal, Transact menu, Multi-SIP
    │   ├── multisip_landing_page.py             # Invest now, Do it yourself (DIY)
    │   ├── multisip_diy_page.py                 # Fund Explorer (+ buttons), T+6 date, Folio, Start Multi-SIP
    │   ├── multisip_payment_page.py             # ROTM Mandate, Bank account, Amount, Proceed
    │   ├── billdesk_simulation_page.py          # BillDesk simulation (Success/Failure status)
    │   └── multisip_success_page.py             # Track status, Back to home
    ├── utils/
    │   ├── data_generator.py                    # T+6 date, random mobile, PAN, email
    │   ├── excel_manager.py                     # OpenPyXL execution results manager
    │   ├── excel_utils.py                       # Excel styling and formatting
    │   └── generate_test_cases.py               # Excel test matrix generator
    ├── screenshots/                             # Runtime screenshot outputs per Page Object
    └── tests/
        ├── test_multisip_flow.py                # Master Pytest E2E Multi-SIP user journey
        └── run_excel_tests.py                   # Excel test suite runner
```

---

## 🛠️ Quick Start

### 1. Initialize Virtual Environment & Install Dependencies
```bash
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
playwright install chromium
```

### 2. Execute End-to-End Multi-SIP Live Test (Headed + SlowMo)
```bash
python -m pytest multisip_test/tests/test_multisip_flow.py --headed --slowmo 500
```

### 3. Generate & Run Excel Data-Driven Suite
```bash
# Generate Excel Test Matrix:
python multisip_test/utils/generate_test_cases.py

# Run Data-Driven Test Execution:
python multisip_test/tests/run_excel_tests.py
```

# Multi-SIP Automation Framework (Playwright + Python)

Enterprise-grade Page Object Model (POM) automation framework for the **Aditya Birla Sun Life Mutual Fund (ABSLMF) Multi-SIP Journey**.

---

## 🚀 Key Framework Features

- **Page Object Model (POM)**: Strict separation of locators and actions across dedicated screens (`LoginPage`, `DashboardPage`, `MultiSipLandingPage`, `MultiSipDiyPage`, `MultiSipPaymentPage`, `BilldeskSimulationPage`, `MultiSipSuccessPage`). Zero raw selectors inside test scripts.
- **Single Centralized Configuration & Dependencies**: Consolidated root [`conftest.py`](conftest.py) for all Pytest fixtures, viewport maximization, and screenshot controls, with a single [`requirements.txt`](requirements.txt) at project root.
- **Centralized URL & Environment Routing**: All URLs, domains, and parameterized endpoints are managed centrally in `data/urls.py` with instant environment switching (`LOCAL`, `QA`, `UAT`, `PROD`).
- **Desktop Window Maximization**: Solves viewport clipping and responsive hamburger menus by combining `no_viewport=True` on browser context with `--start-maximized` browser arguments in `conftest.py`.
- **Global Reduced Motion & Unblurred Screenshots**: 
  - `conftest.py` configures `"reduced_motion": "reduce"` on the browser context so Tailwind and Radix UI automatically disable continuous animations.
  - Autouse fixture `enforce_screenshot_no_animations` automatically injects `animations="disabled"` and `full_page=True` on every screenshot call in all modes (headed, headless, CI/CD).
  - Autouse fixture `capture_screenshot_on_failure` automatically captures full-page evidence screenshots when any test fails.
- **T+6 Business Day Logic**: Built-in dynamic date calculator (`calculate_t_plus_days(days=6, skip_weekends=True)`) to ensure selected SIP start dates always land on valid trading/banking weekdays (Monday–Friday) and never on Saturdays or Sundays.
- **Resilient CTA & Radix UI Handling**:
  - `Start Multi-SIP` button handles dynamic states, waiting for `:not([disabled])` pre-conditions (Terms & Conditions consent) with multi-stage native click and JavaScript DOM fallback.
  - Accordion auto-expansion for Folio selection and Recurring / One-Time Mandate (ROTM) bank selection.
  - Sequential 4-digit split OTP entry with event binding delays.
- **Data-Driven Excel Execution**: Scaffolds comprehensive test matrices (`generate_test_cases.py`) and executes them via `run_excel_tests.py`, recording PASS/FAIL outcomes, execution timestamps, and screenshot evidence without mutating templates.
- **Master Plan PDF Generator**: Single-command PDF export (`python generate_pdf.py`) converting the comprehensive architecture plan into a publication-ready blueprint for other investment journeys (Lumpsum, STP, SWP).

---

## 📁 Project Structure

```text
MultiSIP/
├── .agents/
│   └── AGENTS.md                                # Persistent AI & developer rules and SPA locator tips
├── .env.example                                 # Template for environment variables
├── .gitignore                                   # Excludes Python artifacts, test outputs, and screenshots
├── requirements.txt                             # Consolidated project dependencies
├── conftest.py                                  # Consolidated Pytest fixtures, viewport config & screenshot interceptors
├── command.txt                                  # Quick CLI execution cheat sheet
├── uat script.txt                               # Verbatim manual test specifications / BRD notes
├── generate_pdf.py                              # Master Architecture PDF generator
├── README.md                                    # Framework documentation
├── implementation_plans/                        # Master blueprint HTML & documentation
│   ├── Multi_Project_Automation_Framework_Master_Plan.html
│   └── README.md
└── multisip_test/
    ├── data/
    │   ├── __init__.py
    │   ├── urls.py                              # Central AppURLs (LOCAL, QA, UAT, PROD)
    │   └── test_data.py                         # TestData constants & .env overrides
    ├── pages/
    │   ├── __init__.py                          # Central export of active Multi-SIP Page Objects
    │   ├── base_page.py                         # Playwright wrapper with auto-screenshots & safe clicks
    │   ├── login_page.py                        # PAN, Terms, Continue, 4-digit OTP
    │   ├── dashboard_page.py                    # Nominee modal dismissal, Transact menu, Multi-SIP
    │   ├── multisip_landing_page.py             # Invest now, Do it yourself (DIY)
    │   ├── multisip_diy_page.py                 # Fund Explorer (+ buttons), T+6 date, Folio, Start Multi-SIP
    │   ├── multisip_payment_page.py             # ROTM Mandate, Bank account, Amount, Proceed
    │   ├── billdesk_simulation_page.py          # BillDesk simulation (Success/Failure status)
    │   └── multisip_success_page.py             # Track status, Back to home
    ├── utils/
    │   ├── __init__.py
    │   ├── data_generator.py                    # T+6 date, random mobile, PAN, email
    │   ├── excel_manager.py                     # OpenPyXL execution results manager
    │   ├── excel_utils.py                       # Excel styling and formatting
    │   └── generate_test_cases.py               # Excel test matrix generator
    ├── screenshots/                             # Runtime screenshot outputs per Page Object (git-ignored)
    └── tests/
        ├── test_multisip_flow.py                # Master Pytest E2E Multi-SIP user journey
        └── run_excel_tests.py                   # Data-driven Excel test suite runner
```

---

## 🛠️ Quick Start

### 1. Initialize Virtual Environment & Install Dependencies
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install framework requirements
pip install -r requirements.txt
playwright install chromium
```

### 2. Run Interactive Live Test (Headed + SlowMo)
```powershell
python -m pytest multisip_test/tests/test_multisip_flow.py --headed --slowmo 500
```

### 3. Run Headless Execution (for CI/CD or Background Runner)
```powershell
# Windows PowerShell:
$env:HEADLESS="true"; python -m pytest multisip_test/tests/test_multisip_flow.py

# Linux/macOS:
HEADLESS=true python -m pytest multisip_test/tests/test_multisip_flow.py
```

### 4. Target Specific Environment (LOCAL, QA, UAT, PROD)
```powershell
# Via Pytest CLI Option:
python -m pytest multisip_test/tests/test_multisip_flow.py --headed --env=QA

# Via Environment Variable:
$env:TEST_ENV="QA"; python -m pytest multisip_test/tests/test_multisip_flow.py --headed
```

### 5. Generate & Run Excel Data-Driven Suite
```powershell
# Generate Excel Test Matrix:
python multisip_test/utils/generate_test_cases.py

# Run Data-Driven Test Execution:
python multisip_test/tests/run_excel_tests.py
```

### 6. Export Master Implementation Plan to PDF
```powershell
python generate_pdf.py
```

---

## 🛡️ Best Practices & Architecture Rules

1. **No Raw Selectors in Tests**: All locators live exclusively in `pages/*_page.py`.
2. **Centralized URLs**: Never hardcode domains or paths; import from `data.urls.AppURLs`.
3. **Unblurred Evidence**: All screenshot capture calls automatically enforce `animations="disabled"` and `full_page=True`.
4. **Git Cleanliness**: All screenshots (`screenshots/`, `**/screenshots/`, `*.png`) are ignored by `.gitignore` to prevent repository bloat.

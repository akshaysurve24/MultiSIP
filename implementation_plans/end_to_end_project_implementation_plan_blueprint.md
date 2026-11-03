# End-to-End Test Automation Framework: Complete Implementation Blueprint

> [!NOTE]
> This document serves as the **master architecture, folder hierarchy, and step-by-step implementation blueprint** for building enterprise-grade, reusable Playwright + Python automation frameworks for any web application (with specialized optimizations for Angular, React, and Vue applications).

---

## 📂 1. Exact Folder Hierarchy

When setting up a new automation project, recreate this exact folder and file structure:

```text
<Project_Root>/
│
├── .agents/
│   └── AGENTS.md                    # Framework automation rules, lessons learned & locator strategies
│
├── multisip_test/                   # Main test suite package
│   │
│   ├── conftest.py                  # Pytest fixtures, viewport configuration & browser launch options
│   ├── requirements.txt             # Python dependencies (playwright, pytest, openpyxl, faker)
│   ├── generate_test_cases.py       # Scaffolding engine to generate structured Excel test cases
│   ├── command.txt                  # CLI quick-reference cheat sheet for running tests
│   ├── uat script.txt               # Manual test requirements / original test specification notes
│   │
│   ├── data/
│   │   ├── __init__.py
│   │   ├── urls.py                  # Centralized base domains, route paths, full URLs & dynamic route builders
│   │   └── test_data.py             # Default test constants, form inputs, static values, credentials
│   │
│   ├── pages/                       # Page Object Model (POM) Layer
│   │   ├── __init__.py
│   │   ├── base_page.py             # Core Playwright wrapper (js_click, slow_fill, full-page screenshots)
│   │   ├── login_page.py            # Login, PAN entry, Terms checkbox, 4-digit OTP entry
│   │   ├── dashboard_page.py        # Nominee regulatory popup, Transact button, Multi-SIP menu item
│   │   ├── multisip_landing_page.py # Multi-SIP landing: Invest now, Do it yourself
│   │   ├── multisip_diy_page.py     # Funds selection, T+2 start date, Step-up options, Folio toggle, OTP
│   │   ├── multisip_payment_page.py # ROTM selection, Bank dropdown, Mandate amount, Proceed
│   │   ├── billdesk_simulation_page.py # BillDesk simulator (Success/Failure status, Submit)
│   │   └── multisip_success_page.py # Success confirmation, Track Status, Back to Home
│   │
│   ├── utils/                       # Shared Utilities
│   │   ├── __init__.py
│   │   ├── data_generator.py        # Dynamic test data generators (T+2 date, random mobile, PAN, email)
│   │   ├── excel_manager.py         # OpenPyXL manager for reading/writing execution statuses & formatting
│   │   └── excel_utils.py           # Additional excel helpers, formula handlers, cell stylers
│   │
│   ├── screenshots/                 # Auto-generated runtime screenshots organized by Page Object name
│   │
│   └── tests/                       # Test Runners Layer
│       ├── __init__.py
│       ├── test_multisip_flow.py    # Pytest E2E live visual test suite (headed / slowmo execution)
│       └── run_excel_tests.py       # Data-driven background execution engine running test cases from Excel
│
├── command.txt                      # CLI quick-reference cheat sheet for running tests
├── uat script.txt                   # Manual test requirements / original test specification notes
└── implementation_plans/            # Architectural blueprints & implementation guides
```


# MultiSIP Test Automation Framework — Agent Rules & Knowledge Base

This document records architectural principles, golden rules, locator strategies, and lessons learned for developers and AI agents maintaining this automation framework.

---

## 1. Core Architectural Rules

1. **Centralized URLs**:
   - Never hardcode environment hostnames or route paths directly inside Page Objects or test files.
   - All URLs, routes, and parameterized path builders must reside inside `data/urls.py` (`AppURLs`).
   - Switch target test tiers via `TEST_ENV=QA` or `TEST_ENV=UAT` (defaults to UAT).

2. **Page Object Model (POM)**:
   - Every page/modal screen owns a dedicated Page Object inheriting from `BasePage`.
   - Locators and UI manipulation belong exclusively to Page Objects.
   - Test files (`tests/test_*.py`) must read like clean, linear user journeys and never contain raw selectors.

3. **Separate Test Data & Secrets**:
   - Default test values, labels, and constants live in `data/test_data.py`.
   - Dynamic non-colliding fields (e.g. mobile, email) are generated via `utils/data_generator.py`.
   - Sensitive credentials, PAN numbers, OTPs, or bank details are loaded from environment variables (`.env`) with safe defaults.
   - Never commit live or real financial information.

4. **Full-Page & Traceable Screenshots**:
   - Every screenshot must capture the entire DOM using `full_page=True, animations="disabled"`.
   - Screenshots are automatically organized into subdirectories named after the calling Page Object class:
     `screenshots/<PageClassName>/<action>_<timestamp>.png`.
   - Directories are created dynamically.

5. **Desktop Maximization & Viewport Management**:
   - In `conftest.py`, `no_viewport=True` is set on the browser context alongside `--start-maximized`.
   - This ensures modern responsive frameworks (Tailwind, Radix UI) render the full desktop layout instead of mobile hamburger bars.

---

## 2. Golden Rules for Modern SPAs (Angular / React / Radix UI)

1. **Avoid Strict Mode Violations**:
   - Modern SPAs frequently render desktop and mobile layouts in parallel or keep hidden elements in the DOM.
   - Scope locators to visible elements using `>> visible=true` or select the exact interactive control by role/attribute.
   - Prefer semantic attributes: `aria-label`, `role`, and unique IDs.

2. **Handling Overlays & Dialog Interceptions**:
   - Modals (such as the regulatory nominee popup), sticky headers, and backdrop overlays can intercept clicks.
   - When native Playwright `.click()` is obstructed, use `BasePage.js_click(selector)`:
     `self.page.locator(selector).evaluate("node => node.click()")`.

3. **Custom Checkbox and Switch Controls**:
   - Buttons with `role="checkbox"` (e.g., Radix UI primitives) store state in `data-state="checked"` or `data-state="unchecked"` and `aria-checked="true"|"false"`.
   - Check state before clicking to avoid unchecking an already selected box.

4. **Multi-Fund Selection Pattern**:
   - In the DIY Explore Funds section, each fund card displays a title `<h2>` and a plus button `<button aria-label="Add to selection">`.
   - Locate the parent card or sibling relative to the fund title to ensure the exact fund's `+` button is clicked.

5. **Date Selection (T+6 Business Logic)**:
   - SIP start date requires at least T+6 days from today's date.
   - Format: `DD/MM/YYYY` (e.g. `10/11/2026`).
   - Use dynamic calculation helper `calculate_t_plus_days(6)`.

6. **Accordions & Animated Drawers**:
   - Folio selection and ROTM bank selection use Radix collapsible accordions (`[data-state="closed"]` -> `[data-state="open"]`).
   - Click the header, wait for content expansion (`[data-state="open"]`), then click the desired item.

7. **OTP 4-Digit Split Inputs**:
   - Each digit has its own input (`aria-label="OTP digit 1"`, `2`, `3`, `4`).
   - Fill each digit sequentially with a slight pause to allow keyboard event bindings to trigger.

---

## 3. Maintenance Checklist

- [ ] Check if DOM IDs or `aria-label`s changed in latest deployment.
- [ ] Ensure `data/urls.py` reflects any new query parameters or route restructuring.
- [ ] Verify both headed visual debugging and headless CI/CD execution succeed.
- [ ] Verify test results write back to Excel correctly via `tests/run_excel_tests.py`.


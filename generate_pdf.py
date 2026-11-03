import os
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def generate_implementation_plan_pdf():
    """
    Converts the Master Implementation Plan HTML document into a publication-ready
    PDF using Playwright's headless Chromium print engine.
    """
    project_root = Path(__file__).resolve().parent
    plans_dir = project_root / "implementation_plans"

    html_file = plans_dir / "Multi_Project_Automation_Framework_Master_Plan.html"
    pdf_file = plans_dir / "Multi_Project_Automation_Framework_Master_Plan.pdf"

    if not html_file.exists():
        raise FileNotFoundError(f"HTML master plan not found at: {html_file}")

    print(f"Reading HTML source: {html_file}")
    print("Launching Chromium PDF generator...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(html_file.as_uri(), wait_until="networkidle")
        page.pdf(
            path=str(pdf_file),
            format="A4",
            print_background=True,
            margin={
                "top": "15mm",
                "bottom": "15mm",
                "left": "15mm",
                "right": "15mm",
            },
        )
        browser.close()

    print(f"SUCCESS: Master Implementation Plan PDF generated at:\n{pdf_file}")
    return str(pdf_file)


if __name__ == "__main__":
    generate_implementation_plan_pdf()


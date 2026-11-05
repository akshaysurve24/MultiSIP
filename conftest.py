import os
import sys
import time
from pathlib import Path
import pytest

# 1. Ensure package directories resolve cleanly in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
MULTISIP_TEST_DIR = PROJECT_ROOT / "multisip_test"

for directory in (MULTISIP_TEST_DIR, PROJECT_ROOT):
    dir_str = str(directory)
    if dir_str not in sys.path:
        sys.path.insert(0, dir_str)

# 2. Optionally load environment variables from .env if python-dotenv is installed
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def pytest_addoption(parser):
    """Add command line options for runtime customization."""
    parser.addoption(
        "--env",
        action="store",
        default=os.getenv("TEST_ENV", "UAT"),
        help="Target test environment: LOCAL, QA, UAT, PROD",
    )


@pytest.fixture(scope="session", autouse=True)
def set_test_env(pytestconfig):
    """Ensure TEST_ENV environment variable reflects the active session."""
    env = pytestconfig.getoption("env").upper()
    os.environ["TEST_ENV"] = env
    return env


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """
    Disable emulated fixed viewport so the browser window determines dimensions.
    This prevents desktop controls from collapsing into mobile hamburger menus on modern SPAs.
    Also enables 'reduced_motion' so CSS animations and transitions are minimized globally.
    """
    return {
        **browser_context_args,
        "no_viewport": True,
        "reduced_motion": "reduce",
    }


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """
    Launch browser fully maximized to mimic real end-user desktop resolution.
    Headed by default for interactive review, or headless via HEADLESS=true.
    """
    is_headless = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")
    return {
        **browser_type_launch_args,
        "headless": is_headless,
        "args": ["--start-maximized"],
    }


# ---------------------------------------------------------------------------
# SCREENSHOT FIXTURES & ANIMATION CONTROLS (HEADED, HEADLESS, ALL MODES)
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def enforce_screenshot_no_animations(page):
    """
    Autouse fixture that automatically enforces 'animations="disabled"'
    and 'full_page=True' on every page.screenshot() call across all tests,
    page objects, and execution modes (headed, headless, CI/CD).
    """
    original_screenshot = page.screenshot

    def patched_screenshot(*args, **kwargs):
        # Enforce animations="disabled" unless explicitly overridden
        kwargs.setdefault("animations", "disabled")
        kwargs.setdefault("full_page", True)
        return original_screenshot(*args, **kwargs)

    page.screenshot = patched_screenshot
    yield page


@pytest.fixture
def capture_screenshot(page):
    """
    Reusable test fixture to capture a clean, unblurred full-page screenshot
    with animations disabled on demand from any test:
    
    Usage in test:
        def test_flow(page, capture_screenshot):
            capture_screenshot("step_name", folder="MyModule")
    """
    def _capture(name: str = "step", folder: str = "ManualScreenshots") -> str:
        screenshot_dir = PROJECT_ROOT / "screenshots" / folder
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        timestamp = int(time.time() * 1000)
        screenshot_path = screenshot_dir / f"{name}_{timestamp}.png"

        page.screenshot(
            path=str(screenshot_path),
            full_page=True,
            animations="disabled",
        )
        print(f"[SCREENSHOT CAPTURED] {screenshot_path}")
        return str(screenshot_path)

    return _capture


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test execution status for failure screenshots."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(autouse=True)
def capture_screenshot_on_failure(request, page):
    """
    Autouse fixture that automatically captures a full-page, unblurred
    screenshot with animations disabled whenever a test fails.
    Saved to screenshots/Failures/<test_name>_<timestamp>.png.
    """
    yield
    rep_call = getattr(request.node, "rep_call", None)
    rep_setup = getattr(request.node, "rep_setup", None)
    if (rep_call and rep_call.failed) or (rep_setup and rep_setup.failed):
        failure_dir = PROJECT_ROOT / "screenshots" / "Failures"
        failure_dir.mkdir(parents=True, exist_ok=True)
        timestamp = int(time.time() * 1000)
        safe_test_name = request.node.name.replace("/", "_").replace(":", "_").replace(" ", "_")
        failure_path = failure_dir / f"FAILED_{safe_test_name}_{timestamp}.png"
        try:
            page.screenshot(
                path=str(failure_path),
                full_page=True,
                animations="disabled",
            )
            print(f"\n[FAILURE SCREENSHOT SAVED] {failure_path}")
        except Exception as e:
            print(f"\n[WARNING] Could not capture failure screenshot: {e}")

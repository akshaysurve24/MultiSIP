import os
import sys
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
    """
    return {
        **browser_context_args,
        "no_viewport": True,
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

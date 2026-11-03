# Playwright Viewport & Window Maximization Fix

## The Problem
By default, Playwright creates a browser context with an emulated 1280x720 viewport inside a standard window. 
In modern responsive frameworks (Tailwind, Bootstrap, Angular Material):
- Desktop navigation links collapse into mobile hamburger menus when screen width is under standard breakpoints (e.g., 1440px or 1920px).
- Transact buttons, multi-column tables, and summary sidebars hide behind collapsible drawer controls.
- Passing `["--start-maximized"]` alone does not fix this if Playwright's emulated viewport still limits the rendered area to 1280x720.

## The Fix
In Pytest's `conftest.py`, both the browser launch arguments and the context arguments must be configured simultaneously:

```python
import os
import pytest

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Disable emulated fixed viewport so the browser window determines dimensions."""
    return {
        **browser_context_args,
        "no_viewport": True
    }

@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    """Launch the browser fully maximized to mimic real end-user desktop resolution."""
    is_headless = os.getenv("HEADLESS", "false").lower() in ("true", "1", "yes")
    return {
        **browser_type_launch_args,
        "headless": is_headless,       # Configurable, headed by default for interactive review
        "args": ["--start-maximized"]   # Launch fully maximized
    }
```

## Result
The browser opens seamlessly maximized to the physical monitor resolution (e.g. 1920x1080), rendering the true desktop application layout without responsive layout clipping.

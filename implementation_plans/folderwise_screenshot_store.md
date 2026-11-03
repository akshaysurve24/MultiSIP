# Folder-Wise Screenshot Storage Architecture

## Overview
Automated test artifacts should be clean, traceable, and segregated by application domain. Dumping hundreds of runtime screenshots into a single flat directory makes debugging tedious. 

The framework automatically introspects the active Page Object class name (`self.__class__.__name__`) at runtime and creates dedicated subdirectories under `screenshots/`:

```text
screenshots/
├── LoginPage/
│   ├── navigation_1710001000.png
│   └── enter_pan_1710001002.png
├── DashboardPage/
│   ├── dismiss_nominee_1710001005.png
│   └── click_sip_1710001007.png
├── MultiSipDiyPage/
│   ├── select_fund_1710001010.png
│   └── enter_sip_details_1710001015.png
├── MultiSipPaymentPage/
│   └── select_rotm_1710001020.png
└── MultiSipSuccessPage/
    └── order_success_1710001025.png
```

## Implementation Mechanism
Inside `pages/base_page.py`:

```python
import os
import time

class BasePage:
    def take_screenshot(self, name: str) -> str:
        page_name = self.__class__.__name__
        # Locate project root screenshots directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        screenshot_dir = os.path.join(base_dir, "screenshots", page_name)
        os.makedirs(screenshot_dir, exist_ok=True)
        
        timestamp = int(time.time() * 1000)
        screenshot_path = os.path.join(screenshot_dir, f"{name}_{timestamp}.png")
        self.page.screenshot(path=screenshot_path, full_page=True, animations="disabled")
        print(f"Screenshot saved to: {screenshot_path}")
        return screenshot_path
```

## Benefits
- Visual timeline cleanly segregated per page screen.
- Easy audit trails and attachment to test execution reports / Excel matrices.
- Dynamic folder creation prevents any `FileNotFoundError`.

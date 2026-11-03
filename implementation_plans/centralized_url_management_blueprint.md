# Centralized URL Management Blueprint

## Purpose
In enterprise automation suites, hardcoding URLs across test scripts and page objects causes maintenance bottlenecks when switching between development tiers (LOCAL, QA, UAT, PROD) or when route structures change. Centralizing all URL logic in a single file guarantees instant environment portability and route consistency.

## Implementation Details

All URLs and route patterns are maintained in `data/urls.py` via the `AppURLs` class:

```python
import os

class AppURLs:
    ENV_DOMAINS = {
        "LOCAL": "http://localhost:3000",
        "QA": "https://investorqa.abslmfbeta.com",
        "UAT": "https://investoruat.abslmfbeta.com",
        "PROD": "https://mutualfund.adityabirlacapital.com",
    }
    
    ACTIVE_ENV = os.getenv("TEST_ENV", "UAT").upper()
    BASE_DOMAIN = ENV_DOMAINS.get(ACTIVE_ENV, ENV_DOMAINS["UAT"])
    PORTAL_PREFIX = "/mf-investor"
    BASE_URL = f"{BASE_DOMAIN}{PORTAL_PREFIX}"

    # Route Paths
    LOGIN_PATH = f"{PORTAL_PREFIX}/login"
    DASHBOARD_PATH = f"{PORTAL_PREFIX}/dashboard"
    MULTISIP_PATH = f"{PORTAL_PREFIX}/multi-sip"
    MULTISIP_DIY_PATH = f"{PORTAL_PREFIX}/multi-sip/diy"
    MULTISIP_PAYMENT_PATH = f"{PORTAL_PREFIX}/multi-sip/payment?type=diy"
    MULTISIP_SUCCESS_PATH = f"{PORTAL_PREFIX}/multi-sip/success"
    EXPLORE_FUNDS_PATH = f"{PORTAL_PREFIX}/explore-funds?investMode=sip&plan=direct&category=all-funds&sort=returns_3y"
    
    # Absolute URLs
    LOGIN_URL = f"{BASE_DOMAIN}{LOGIN_PATH}"
    DASHBOARD_URL = f"{BASE_DOMAIN}{DASHBOARD_PATH}"
    MULTISIP_URL = f"{BASE_DOMAIN}{MULTISIP_PATH}"
    MULTISIP_DIY_URL = f"{BASE_DOMAIN}{MULTISIP_DIY_PATH}"
    MULTISIP_PAYMENT_URL = f"{BASE_DOMAIN}{MULTISIP_PAYMENT_PATH}"
    MULTISIP_SUCCESS_URL = f"{BASE_DOMAIN}{MULTISIP_SUCCESS_PATH}"
    EXPLORE_FUNDS_URL = f"{BASE_DOMAIN}{EXPLORE_FUNDS_PATH}"

    @classmethod
    def get_sip_config_url(cls, scheme_slug: str = "BMF", scheme_code: str = "251GZ") -> str:
        return f"{cls.BASE_URL}/invest/sip/{scheme_slug}?investMode=sip&schemeCode={scheme_code}"

    @classmethod
    def get_payment_url(cls, scheme_slug: str = "AEF") -> str:
        return f"{cls.BASE_URL}/invest/sip/{scheme_slug}/payment?investMode=sip"

    @classmethod
    def get_success_url(cls, scheme_slug: str = "AEF") -> str:
        return f"{cls.BASE_URL}/invest/sip/{scheme_slug}/success"
```

## Benefits
- Switch test target environments across the entire suite using `TEST_ENV=QA pytest`.
- Zero broken links if route prefixes or query parameters change.
- Central dynamic route builders for parameterized scheme codes.

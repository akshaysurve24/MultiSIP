import random
import string
from datetime import datetime, timedelta


def calculate_t_plus_days(days: int = 6, skip_weekends: bool = True) -> str:
    """
    Calculates T + N date formatted as DD/MM/YYYY.
    If skip_weekends is True, adds business days only.
    """
    current_date = datetime.now()
    if not skip_weekends:
        target_date = current_date + timedelta(days=days)
    else:
        added_days = 0
        target_date = current_date
        while added_days < days:
            target_date += timedelta(days=1)
            # Monday=0, Sunday=6
            if target_date.weekday() < 5:
                added_days += 1

    return target_date.strftime("%d/%m/%Y")


def generate_random_mobile() -> str:
    """Generates a random 10-digit Indian mobile number starting with 9, 8, 7, or 6."""
    prefix = random.choice(["9", "8", "7", "6"])
    suffix = "".join(random.choices(string.digits, k=9))
    return f"{prefix}{suffix}"


def generate_random_email() -> str:
    """Generates a unique random email address for safe test usage."""
    random_str = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"uat_multisip_{random_str}@example.com"


def generate_random_pan() -> str:
    """Generates a synthetic valid-format PAN (5 letters + 4 digits + 1 letter)."""
    letters_first = "".join(random.choices(string.ascii_uppercase, k=5))
    digits = "".join(random.choices(string.digits, k=4))
    last_letter = random.choice(string.ascii_uppercase)
    return f"{letters_first}{digits}{last_letter}"


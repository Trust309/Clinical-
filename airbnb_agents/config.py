"""Configuration for the Airbnb Business Agents system."""

# Host information
HOST_NAME = "Your Host"

# Airbnb platform fee percentage (host-only fee is ~3%)
PLATFORM_FEE_PCT = 3.0

# Default pricing rules
DEFAULT_WEEKEND_PREMIUM = 1.20
DEFAULT_WEEKLY_DISCOUNT = 0.90
DEFAULT_MONTHLY_DISCOUNT = 0.75

# Communication timing (hours before/after events)
CHECKIN_INSTRUCTIONS_HOURS_BEFORE = 24
CHECKOUT_REMINDER_HOURS_BEFORE = 18
REVIEW_REQUEST_HOURS_AFTER = 24

# Cleaning
DEFAULT_CLEANING_COST = 75.0

# Inventory thresholds
LOW_INVENTORY_ALERT = True

# Financial
TAX_YEAR = 2025
DEFAULT_CURRENCY = "USD"

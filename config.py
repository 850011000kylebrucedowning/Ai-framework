"""
Configuration settings for Bookkeeping & Payment Management Bot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys & Credentials (replace with actual keys in .env)
FIXER_API_KEY = os.getenv("FIXER_API_KEY", "")  # For currency exchange
OPEN_EXCHANGE_API_KEY = os.getenv("OPEN_EXCHANGE_API_KEY", "")  # Alternative currency API
TREASURY_API_KEY = os.getenv("TREASURY_API_KEY", "")  # US Treasury data

# Database
DATABASE_PATH = os.getenv("DATABASE_PATH", "bookkeeping.db")

# USD Configuration
DEFAULT_CURRENCY = "USD"
SUPPORTED_CURRENCIES = ["USD", "EUR", "GBP", "CAD", "AUD", "JPY", "CNY"]

# Data Validation Rules
MIN_FUND_AMOUNT = 0.01
MAX_FUND_AMOUNT = 999999999.99
ALLOWED_FUND_STATUSES = ["pending", "verified", "cleared", "flagged"]
ALLOWED_CONTRACT_STATUSES = ["draft", "active", "completed", "cancelled"]

# Date Formats
DATE_FORMATS = [
    "%Y-%m-%d",
    "%m/%d/%Y",
    "%d/%m/%Y",
    "%Y/%m/%d",
    "%B %d, %Y",
    "%b %d, %Y",
    "%d-%m-%Y",
    "%m-%d-%Y"
]

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "bookkeeping_bot.log"

# Banking Integration (Future)
BANK_PARTNERS = {
    "stripe_connect": {
        "enabled": False,
        "api_key": os.getenv("STRIPE_API_KEY", ""),
    },
    "synapse": {
        "enabled": False,
        "api_key": os.getenv("SYNAPSE_API_KEY", ""),
    },
    "treasury_prime": {
        "enabled": False,
        "api_key": os.getenv("TREASURY_PRIME_API_KEY", ""),
    }
}

# FDIC Insurance Validation
FDIC_INSURANCE_LIMIT = 250000.00  # Per account, per bank

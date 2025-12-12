"""
Configuration module for the Digital Taximeter application.

This module is responsible for:
- Resolving base project directories
- Managing data storage paths
- Setting up application-wide logging
- Loading fare rate configuration from JSON files
"""

import json
import logging
import os

"""
Resolve base directory paths.

BASE_DIR:
    Root directory of the project.
    Example:
        .../project/src/config.py
        -> BASE_DIR = .../project

DATA_DIR:
    Directory where runtime data is stored (logs, JSON files, etc.)
"""
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

"""
Ensure that the data directory exists.

If the directory does not exist, it will be created automatically
to prevent runtime errors when writing logs or data files.
"""
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

"""
File paths used by the application.
"""
LOG_PATH = os.path.join(DATA_DIR, "taximetro.log")
RATES_PATH = os.path.join(DATA_DIR, "rates.json")

"""
Default fare rates.

Keys:
    "1" -> moving state
    "2" -> stopped state
Values:
    price per second
"""
DEFAULT_RATES = {"1": 0.05, "2": 0.02}


def setup_logging():
    """
    Configure global logging settings for the application.

    - Logs are written to both a file and the console.
    - Log level is set to INFO.
    - UTF-8 encoding is enforced for file logs.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )


def load_rates():
    """
    Load fare rates from the rates configuration file.

    Behavior:
    - If the rates file does not exist, default rates are used.
    - Missing rate keys are automatically filled with defaults.
    - Any error during loading falls back to default rates.

    Returns:
        dict: Dictionary containing fare rates per state.
    """
    if not os.path.exists(RATES_PATH):
        logging.info(f"{RATES_PATH} not found. Using default rates.")
        return DEFAULT_RATES.copy()

    try:
        with open(RATES_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)

        for k, v in DEFAULT_RATES.items():
            data.setdefault(k, v)

        logging.info(f"Loaded rates: {data}")
        return data

    except Exception:
        logging.exception("Error loading rates. Using default rates.")
        return DEFAULT_RATES.copy()
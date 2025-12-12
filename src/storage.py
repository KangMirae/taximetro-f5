"""
storage.py

Persistence layer for trip history.

This module provides HistoryManager, which:
- Ensures the trip history file exists
- Saves completed trips to JSON
- Loads the complete trip history list
"""

import json
import logging
import os
from datetime import datetime


# Build the default path to the trip history file.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_PATH = os.path.join(BASE_DIR, "data", "trip_history.json")


class HistoryManager:
    """
    Manage trip history storage in a JSON file.

    Attributes:
        filepath (str): Path to the JSON file used to store trip history.
    """

    def __init__(self, filepath: str = HISTORY_PATH):
        """
        Initialize the history manager and ensure the file exists.

        Args:
            filepath (str): Path to the trip history JSON file.
        """
        self.filepath = filepath
        self._ensure_file()

    def _ensure_file(self) -> None:
        """
        Create the history file if it does not exist.

        The file is initialized as an empty JSON list: [].

        Returns:
            None
        """
        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump([], f)

    def save_trip(self, customer_name: str, total_fare: float) -> None:
        """
        Save a completed trip record into the history file.

        The newest record is inserted at the beginning of the list (index 0)
        so that the history is naturally ordered by most recent first.

        Args:
            customer_name (str): Customer name for the trip.
            total_fare (float): Final fare for the trip.

        Returns:
            None
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_record = {
            "date": timestamp,
            "name": customer_name,
            "fare": round(total_fare, 2),
        }

        try:
            # Read existing data.
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Insert new data at the top (latest first).
            data.insert(0, new_record)

            # Write back to file.
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            logging.info(f"Saved trip: {new_record}")

        except Exception:
            logging.exception("Error saving trip history.")

    def get_all_trips(self) -> list:
        """
        Load the full list of trip history records.

        Returns:
            list: Trip record list. Returns an empty list on error.
        """
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
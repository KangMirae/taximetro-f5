"""
taximeter.py

Core taximeter domain logic.

This module defines Taximeter, which tracks a single active trip:
- Moving / stopped state
- Fare accumulation based on base rates, level multipliers, and surcharge options
- Log events for UI display
- Provide live snapshot data for the frontend (fare, state, logs, meta info)
"""

import logging
import time
from datetime import datetime


class Taximeter:
    """
    A taximeter that calculates fares over time based on configurable rules.

    The configuration is expected to follow the structure of rates.json:
    - base_rates: base €/sec rates for moving and stopped states
    - levels: multipliers per fare level
    - options: surcharge options with multipliers (e.g., city, night)

    Attributes:
        config (dict): Full configuration dictionary (raw).
        base_rates (dict): Base rates by state key ("1"=move, "2"=stop).
        level_multipliers (dict): Multipliers by level key (string).
        option_config (dict): Options dictionary (with name/multiplier).
        is_running (bool): Whether a trip is currently active.
        current_state (str): "1" for moving, "2" for stopped.
        total_fare (float): Accumulated fare (without "live" current segment).
        last_update_time (float): Last timestamp used for fare accumulation.
        current_level (str): Current fare level (string for JSON key access).
        active_options (dict): Active status for options (e.g., city/night).
        logs (list): List of log entries for UI display.
    """

    def __init__(self, config_data: dict):
        """
        Initialize the Taximeter with a configuration dictionary.

        Args:
            config_data (dict): Full configuration dictionary (rates.json style).
        """
        self.config = config_data
        self.base_rates = config_data.get("base_rates", {"1": 0.05, "2": 0.02})
        self.level_multipliers = config_data.get("levels", {"1": 1.0})
        self.option_config = config_data.get("options", {})

        # Runtime state
        self.is_running = False
        self.current_state = "2"  # "1": Move, "2": Stop
        self.total_fare = 0.0
        self.last_update_time = 0.0

        # Current settings
        self.current_level = "1"
        self.active_options = {"city": False, "night": False}
        self.logs = []

    def start_journey(self, level: int = 1) -> None:
        """
        Start a new trip and reset internal state.

        The trip begins in the "moving" state.

        Args:
            level (int): Fare level selected by the user.

        Returns:
            None
        """
        self.is_running = True
        self.total_fare = 0.0
        self.current_level = str(level)  # Convert to string for JSON-key access
        self.active_options = {"city": False, "night": False}
        self.logs = []

        self.current_state = "1"
        self.last_update_time = time.time()

        self._add_log(f"Trip Started (Lv.{self.current_level})")
        logging.info(f"Trip started. Level: {self.current_level}")

    def change_state(self) -> None:
        """
        Toggle between moving and stopped state.

        This method accumulates fare up to the moment of switching states.

        Returns:
            None
        """
        if not self.is_running:
            return

        self._accumulate_fare()

        if self.current_state == "1":
            self.current_state = "2"
            self._add_log("Taxi Stopped")
        else:
            self.current_state = "1"
            self._add_log("Taxi Moving")

        self.last_update_time = time.time()

    def toggle_option(self, option_key: str, is_active: bool) -> None:
        """
        Enable or disable a surcharge option (e.g., city/night).

        This method accumulates fare up to the moment of toggling the option.

        Args:
            option_key (str): Option id in the config (e.g., "city", "night").
            is_active (bool): True to enable, False to disable.

        Returns:
            None
        """
        if not self.is_running:
            return

        self._accumulate_fare()

        self.active_options[option_key] = is_active
        self.last_update_time = time.time()

        status = "ON" if is_active else "OFF"
        opt_name = self.option_config.get(option_key, {}).get("name", option_key)
        self._add_log(f"{opt_name} {status}")

    def _get_multiplier(self) -> float:
        """
        Compute the combined multiplier for the current level + active options.

        Returns:
            float: Combined multiplier.
        """
        # 1) Level multiplier
        mult = self.level_multipliers.get(self.current_level, 1.0)

        # 2) Option multipliers
        for key, active in self.active_options.items():
            if active:
                opt_val = self.option_config.get(key, {}).get("multiplier", 1.0)
                mult *= opt_val

        return mult

    def _accumulate_fare(self) -> float:
        """
        Accumulate fare from last_update_time up to now using current state.

        Returns:
            float: The 'now' timestamp used for accumulation.
        """
        now = time.time()
        duration = now - self.last_update_time

        base = self.base_rates.get(self.current_state, 0.0)
        multiplier = self._get_multiplier()

        self.total_fare += duration * (base * multiplier)
        return now

    def get_live_data(self) -> dict:
        """
        Return a live snapshot for the UI (fare, state, logs, meta).

        This includes:
        - Real-time fare (including the current ongoing segment duration)
        - State ("1" moving / "2" stopped)
        - Logs for UI display
        - Meta info (level, derived move/stop rates, active options)

        Returns:
            dict: Live snapshot data for the frontend.
        """
        current_total = self.total_fare

        if self.is_running:
            now = time.time()
            duration = now - self.last_update_time
            base = self.base_rates.get(self.current_state, 0.0)
            mult = self._get_multiplier()
            current_total += duration * (base * mult)

        # UI display rates (level applied, options excluded)
        lvl_mult = self.level_multipliers.get(self.current_level, 1.0)
        display_move = self.base_rates["1"] * lvl_mult
        display_stop = self.base_rates["2"] * lvl_mult

        return {
            "fare": round(current_total, 2),
            "state": self.current_state,
            "logs": self.logs,
            "is_running": self.is_running,
            "meta": {
                "level": self.current_level,
                "move_rate": round(display_move, 3),
                "stop_rate": round(display_stop, 3),
                "active_options": [
                    f"{v['name']} x{v['multiplier']}"
                    for k, v in self.option_config.items()
                    if self.active_options.get(k)
                ],
            },
        }

    def stop_journey(self) -> float:
        """
        Finish the trip and return the final fare.

        Returns:
            float: Final accumulated fare.
        """
        if not self.is_running:
            return 0.0

        self._accumulate_fare()
        self.is_running = False
        self._add_log("Trip Finished")
        return self.total_fare

    def _add_log(self, msg: str) -> None:
        """
        Add a log entry to the top of the list (most recent first).

        Args:
            msg (str): Log message.

        Returns:
            None
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.logs.insert(0, {"time": timestamp, "msg": msg})
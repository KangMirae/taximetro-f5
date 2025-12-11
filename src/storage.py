import logging
import os
from datetime import datetime

# config와 동일하게 data 폴더 경로 계산
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_PATH = os.path.join(BASE_DIR, "data", "trip_history.txt")

class HistoryManager:
    def __init__(self, filepath=HISTORY_PATH): # 기본값을 data 폴더 경로로 설정
        self.filepath = filepath

    def save_trip(self, customer_name, total_fare):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"{timestamp} | {customer_name} | {total_fare:.2f}\n"

        try:
            with open(self.filepath, "a", encoding="utf-8") as f:
                f.write(line)
            logging.info(f"Saved trip history to {self.filepath}: {line.strip()}")
        except Exception:
            logging.exception("Error saving trip history.")
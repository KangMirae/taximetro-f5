import json
import logging
import os

# 현재 파일(config.py)의 위치를 기준으로 상위 폴더의 data 폴더 경로를 찾음
# 예: .../project/src/config.py -> .../project/data/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

# data 폴더가 없으면 자동으로 생성 (에러 방지)
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

LOG_PATH = os.path.join(DATA_DIR, "taximetro.log")
RATES_PATH = os.path.join(DATA_DIR, "rates.json")

DEFAULT_RATES = {"1": 0.05, "2": 0.02}

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_PATH, encoding="utf-8"), # 경로 변경
            logging.StreamHandler()
        ]
    )

def load_rates():
    # RATES_PATH 변수 사용
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
        logging.exception("Error loading rates. Using defaults.")
        return DEFAULT_RATES.copy()
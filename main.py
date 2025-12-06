import time
import logging
import json
import os
from datetime import datetime


# ---------- rate 외부에서 불러오기 ----------
# 기본 요금 (파일이 없을 때 사용할 값)
DEFAULT_RATES = {"1": 0.05, "2": 0.02}

# 실제로 사용할 요금값
RATES = None

def load_rates(config_path="rates.json"):
    '''
    Load dynamic pricing rates from an external JSON configuration file.

    Parameters:
        config_path (str): Path to the JSON file containing rate settings.

    Behavior:
        - If the file exists, loads rates for:
            '1' → moving rate (€/sec)
            '2' → stopped rate (€/sec)
        - If the file does not exist or is invalid, default rates are used.
        - Ensures all expected keys exist by falling back to default values.

    Returns:
        dict: A dictionary containing the final rates to be used by the program.

    Notes:
        - This function enables price configuration based on demand (Nivel Medio).
        - Populates the global RATES variable with validated values.
    '''
    global RATES

    if not os.path.exists(config_path):
        logging.info("rates.json not found. Using default rates.")
        RATES = DEFAULT_RATES.copy()
        return

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        for k, v in DEFAULT_RATES.items():
            data.setdefault(k, v)

        logging.info(f"Loaded rates from {config_path}: {data}")
        RATES = data  # ← 여기서 전역 RATES에 값 넣음
    except Exception:
        logging.exception("Error loading rates config. Using default rates.")
        RATES = DEFAULT_RATES.copy()
        
# ---------- logging ----------
def setup_logging():
    '''
    Configure logging for the entire application.

    Behavior:
        - Logs are written to both console and taximetro.log.
        - Includes timestamps, log levels, and descriptive messages.
        - Enables debugging and traceability of user actions and system states.

    Notes:
        - Required for Nivel Medio logging feature.
        - Automatically called during program startup.
    '''
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler("taximetro.log", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

# ---------- fare calculation ----------
def calc(option, duration):
    '''
    Calculate the fare for a given state and time duration.

    Parameters:
        option (str): 
            '1' → taxi moving  
            '2' → taxi stopped
        duration (float): 
            Time spent in this state (seconds)

    Returns:
        float: Fare calculated using the current configured rate.

    Notes:
        - Rates are loaded dynamically from the external configuration file (rates.json).
        - Uses the global RATES dictionary filled during program initialization.
    '''
    # 전역 RATES에서 요금 읽어오기
    rate = RATES[option]

    fare = duration * rate

    logging.info(
        f"calc() called - option={option}, duration={duration:.2f}s, "
        f"rate={rate}, fare={fare:.2f}"
    )

    return fare

# ---------- trip history saving in txt file ----------
def save_trip_history(customer_name, total_fare, history_path="trip_history.txt"):
    """
    Save a completed trip record into a plain text file.
    한 번의 여정이 끝날 때마다 텍스트 파일에 기록 저장.

    Parameters:
        customer_name (str): Name of the customer taking the trip.
        total_fare (float): Final total fare calculated at the end of the trip.
        history_path (str): File path where trip history will be saved.

    Behavior:
        - Appends a new line for every completed trip.
        - Each entry includes timestamp, customer name, and total fare.
        - Creates the file if it does not exist.

    Format:
        YYYY-MM-DD HH:MM:SS | <customer_name> | <fare>
        형식: YYYY-MM-DD HH:MM:SS | 이름 | 요금
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {customer_name} | {total_fare:.2f}\n"

    try:
        with open(history_path, "a", encoding="utf-8") as f:
            f.write(line)
        logging.info(f"Saved trip history: {line.strip()}")
    except Exception:
        logging.exception("Error saving trip history.")


# ---------- taximeter main logic ----------
def taximetro():
    '''
    Main function for managing the taxi meter system (CLI version).

    - Greets the user and starts the program.
    - Allows user to start a trip.
    - Tracks time for each state: moving and stopped.
    - Calculates fare based on configurable rates.
    - Shows status messages when state changes.
    - Saves trip history to a text file when the trip ends.
    - Allows the user to start a new trip or exit the program.
    '''

    # Welcome message
    print("\n\n----------------------------------------\n" \
    "Digital Taximeter - CLI Version\n" \
    "This program simulates a real taxi meter.\n" \
    "You can start a trip, stop, move again,\n" \
    "and end the journey to calculate the fare.\n" \
    "----------------------------------------\n")
    customer_name = input('Tell us your name: ')
    logging.info(f"New customer: {customer_name}")  # 새 손님 로그

    print("\nWelcome, {}".format(customer_name))
    print("We're starting our journey. Please, fasten your seatbelt!\n")

    # 루프1 시작
    while True:
        print("I'm ready. Should we go? (Y/N)")
        answer = input("> ").strip().upper()
        logging.info(f"User ready answer: {answer}")  # Y/N 입력 기록

        # input validation for departing, 루프1-1
        while answer not in ('Y','N'):
            print("Please enter Y or N.")
            answer = input("> ").strip().upper()
            logging.warning(f"Invalid ready answer, user entered: {answer}")
        
        # Selected 'Y' to departure, taxi started moving
        if answer == 'Y':
            logging.info("Trip starting...")
            state_start_time = time.time()
            fare = 0.0
            prev_option = '1'

            # 루프2 시작
            while True:
                # 여정 선택, User Choose an option. (input) 
                print("\nSelect an option. \n"
                "1. Move\n"
                "2. Stop\n"
                "3. Arrive\n"
                "Please choose a number (1-3)")
                curr_option = input("> ").strip()
                logging.info(f"User selected option: {curr_option}")

                # input validation for choosing options, 루프2-1
                while curr_option not in ('1','2','3'):
                    print("Please enter 1,2, or 3")
                    curr_option = input("> ").strip()
                    logging.warning(f"Invalid trip option, user entered: {curr_option}")

                duration = time.time() - state_start_time # 이전 옵션부터 지금까지의 초 계산

                if curr_option == '3': # 도착일 시
                    print("\nTrip finished!")
                    fare += calc(prev_option, duration)
                    logging.info(
                        f"Trip finished. Last segment option={prev_option}, "
                        f"duration={duration:.2f}s, total fare={fare:.2f}"
                    )
                    print(f"\n----- Total fare is € {fare:.2f} -----")

                    save_trip_history(customer_name, fare) # 여정 저장
                    break # 루프2 종료
                else: # 이동 또는 멈춤일 시
                    fare += calc(prev_option, duration)
                    logging.info(
                        f"State change: {prev_option} -> {curr_option}, "
                        f"segment duration={duration:.2f}s, accumulated fare={fare:.2f}"
                    )

                    if curr_option == '1':
                        print("Taxi is now moving...")
                    elif curr_option == '2':
                        print("Taxi has stopped.")
                    
                    state_start_time = time.time()
                    prev_option = curr_option

        # 출발 N, Ask if user wants to terminate the program
        print(f"\n{customer_name}, are you sure you want to leave? (Y/N)")
        answer = input("> ").strip().upper() 
        logging.info(f"Exit confirmation answer: {answer}")

        # input validation for terminating, 루프3
        while answer not in ('Y','N'): 
            print("Please enter Y or N ")
            answer = input("> ").strip().upper() 
            logging.warning(f"Invalid exit answer, user entered: {answer}")

        if answer == 'Y': 
            print("Thank you!")
            logging.info("User chose to exit the program. Bye!")
            break # 루프1 종료

        elif answer == 'N':
            logging.info("User chose to continue using the program.")
            continue

if __name__ == "__main__":
    # Program entry point:
    # - logging is configured
    # - pricing rates are loaded
    # - the taxi meter system starts
    setup_logging()
    load_rates()
    taximetro()
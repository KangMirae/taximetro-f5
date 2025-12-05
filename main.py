import time
import logging

# ---------- logging ----------
def setup_logging():
    """
    로그를 콘솔 + 파일(taximetro.log) 둘 다에 남긴다.
    """
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

    match option:
        # 이동
        case '1': 
            rate = 0.05
        # 정차
        case '2': 
            rate = 0.02
    fare = duration * rate

    # logging : option, duration
    logging.info(
        f"calc() called - option={option}, duration={duration:.2f}s, "
        f"rate={rate}, fare={fare:.2f}"
    )

    return fare

# ---------- taximeter main logic ----------
def taximetro():

    # Welcome message
    customer_name = input('\n\nTell us your name: ')
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
                    fare += calc(prev_option, duration)
                    logging.info(
                        f"Trip finished. Last segment option={prev_option}, "
                        f"duration={duration:.2f}s, total fare={fare:.2f}"
                    )

                    print(f"\n----- Total fare is € {fare:.2f} -----")
                    break # 루프2 종료
                else: # 이동 또는 멈춤일 시
                    fare += calc(prev_option, duration)
                    logging.info(
                        f"State change: {prev_option} -> {curr_option}, "
                        f"segment duration={duration:.2f}s, accumulated fare={fare:.2f}"
                    )
                    
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
    setup_logging()
    taximetro()
import time

def calc(option, duration):

    match option:
        # 이동
        case '1': 
            rate = 0.05
        # 정차
        case '2': 
            rate = 0.02
    fare = duration * rate

    return fare


def taximetro():

    # Welcome message
    customer_name = input('\n\nTell us your name: ')
    print("Welcome, {}".format(customer_name))
    print("We're starting our journey. Please, fasten your seatbelt!\n")

    # 루프1 시작
    while True:
        # 출발해 말아
        print("I'm ready. Should we go? (Y/N) \n")
        answer = input("> ").strip().upper()
        
        # Selected 'Y' to departure, taxi started moving
        if answer == 'Y':
            state_start_time = time.time()
            fare = 0.0
            prev_option = '1'

            # 루프2 시작
            while True:
                # 여정 선택, User Choose an option. (input) 
                print("Select an option. \n"
                "1. Move\n"
                "2. Stop\n"
                "3. Arrive\n"
                "Please choose a number (1-3)")
                curr_option = input("> ").strip()
                duration = time.time() - state_start_time # 이전 옵션부터 지금까지의 초 계산

                if curr_option == '3': # 도착일 시
                    fare += calc(prev_option, duration)
                    print(f"Total fare is € {fare:.2f} ")
                    break # 루프2 종료
                else: # 이동 또는 멈춤일 시
                    fare += calc(prev_option, duration)
                    state_start_time = time.time()
                    prev_option = curr_option

        # 출발 N, Ask if user wants to terminate the program
        print(f"{customer_name}, are you sure you want to leave? (Y/N) \n")
        answer = input("> ").strip().upper() 

        if answer == 'Y': 
            print("User said Yes.")
            print("Thank you!")
            break # 루프1 종료

        elif answer == 'N':
            print("User said No.")
            continue

        
if __name__ == "__main__":
    taximetro()
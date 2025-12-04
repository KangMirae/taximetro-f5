import time

def calc(option, duration):
    return None

def taximetro():

    # Selected 'Y' to departure, taxi started moving
    if answer == 'Y':
        state_start_time = time.time()
        fare = 0.0
        
        while True: 
            # Here, an event occured. User Chose an option. (input) 
            duration = time.time() - state_start_time # 이전 옵션부터 지금까지의 초 계산
            if option == 3: # 도착일 시
                fare += calc(option, duration)
                print(f"Total fare is {fare} euros. ")
                break
            else: # 이동 또는 멈춤일 시
                fare += calc(option, duration)
                state_start_time = time.time()

    # Ask if user wants to terminate the program
        
if __name__ == "__main__":
    taximetro()
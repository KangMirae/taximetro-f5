import sys
from src.config import setup_logging, load_rates
from src.taximeter import Taximeter
from src.storage import HistoryManager

def main():
    # 1. 초기화
    setup_logging()
    rates = load_rates()
    history_mgr = HistoryManager()
    
    # 2. 환영 메시지
    print("\n----------------------------------------")
    print("Digital Taximeter - OOP Refactored CLI")
    print("----------------------------------------")
    
    customer_name = input('Tell us your name: ')
    print(f"\nWelcome, {customer_name}! Let's start.\n")

    # 3. 메인 루프
    while True:
        # 택시 객체 생성 (손님마다 새로 생성)
        taxi = Taximeter(rates)
        
        start_ans = input("Ready to go? (Y/N) > ").strip().upper()
        if start_ans != 'Y':
            if start_ans == 'N':
                print("Bye!")
                break
            continue

        # 여정 시작
        taxi.start_journey()
        print("Taxi is moving...")

        # 주행 중 루프
        while taxi.is_running:
            print("\nSelect an option:")
            print("1. Move (Keep Moving)")
            print("2. Stop (Wait)")
            print("3. Arrive (Finish)")
            
            choice = input("> ").strip()

            if choice == '1':
                if taxi.current_state != '1':
                    taxi.change_state('1')
                    print("Taxi is now moving.")
                else:
                    print("Still moving...")
                    
            elif choice == '2':
                if taxi.current_state != '2':
                    taxi.change_state('2')
                    print("Taxi stopped (waiting).")
                else:
                    print("Still stopped...")
            
            elif choice == '3':
                # 여정 종료
                final_fare = taxi.stop_journey()
                print(f"\n----- TRIP FINISHED -----")
                print(f"Total fare is € {final_fare:.2f}")
                
                # 기록 저장
                history_mgr.save_trip(customer_name, final_fare)
                break
            
            else:
                print("Invalid option. Try 1, 2, or 3.")

        # 프로그램 종료 여부 묻기
        quit_ans = input(f"\n{customer_name}, do you want to exit program? (Y/N) > ").strip().upper()
        if quit_ans == 'Y':
            print("Thank you. Goodbye!")
            break

if __name__ == "__main__":
    main()
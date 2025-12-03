def calc(option):
   
    return None


def go_or_exit(answer):
    if answer == 'Y':
        print("User said Yes.")
        return True
    
    elif answer == 'N':
        print("User said No.")
        return False


def taximetro():

    # Welcome message
    customer_name = input('\n\nTell us your name: ')
    print("Welcome, {}".format(customer_name))
    print("We're starting our journey. Please, fasten your seatbelt!\n")

    termination = False

    # 전체 루프 시작
    while termination == False:
        
        print("I'm ready. Should we go? (Y/N) \n")
        answer = input("> ").strip().upper()
        # 출발해 말아
        answer_bool = go_or_exit(answer)
        option = 0

        # 출발 Y
        if answer_bool == True: 

            while option != '3':
                # 여정 선택
                print("Select an option. \n"
                "1. Move\n"
                "2. Stop\n"
                "3. Arrive\n"
                "Please choose a number (1-3)")

                option = input("> ").strip()
                calc(option)

        # 출발 N
        else: 
            print(f"{customer_name}, are you sure you want to leave? (Y/N) \n")
            answer = input("> ").strip().upper() 

            if answer == 'Y': 
                print("User said Yes.")
                print("Thank you!")
                termination = True

            elif answer == 'N':
                print("User said No.")
                continue


if __name__ == "__main__":
    taximetro()
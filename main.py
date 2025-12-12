"""
CLI entry point for the Digital Taximeter application.

This module provides a command-line interface version of the taximeter
system using an object-oriented design. It allows a user to start a taxi
journey, change driving states, calculate fares in real time, and store
trip history persistently.

This CLI version shares the same core business logic with the web version.
"""

import sys
from src.config import setup_logging, load_rates
from src.taximeter import Taximeter
from src.storage import HistoryManager


def main():
    """
    Run the Digital Taximeter in CLI mode.

    Workflow:
    1. Initialize logging, rate configuration, and history storage.
    2. Ask for customer name.
    3. Start a taxi journey loop.
    4. Allow state changes (move, stop) and trip termination.
    5. Save trip history when the journey ends.
    6. Ask whether the user wants to exit or start a new trip.
    """

    # Initialize application dependencies
    setup_logging()
    rates = load_rates()
    history_mgr = HistoryManager()

    # Welcome message
    print("\n----------------------------------------")
    print("Digital Taximeter - OOP Refactored CLI")
    print("----------------------------------------")
    print(
        "This is a command-line taxi meter simulation.\n"
        "You can start a trip, switch between moving and stopping states,\n"
        "apply fare rules automatically, and calculate the final fare\n"
        "based on time, fare level, and conditions.\n"
    )
    print("Each trip is recorded and saved to the trip history.\n")

    customer_name = input("Tell us your name: ")
    print(f"\nWelcome, {customer_name}! Let's start your journey.\n")

    # Main application loop
    while True:
        taxi = Taximeter(rates)

        start_ans = input("Ready to go? (Y/N) > ").strip().upper()
        if start_ans != "Y":
            if start_ans == "N":
                print("Bye!")
                break
            continue

        # Start the journey
        taxi.start_journey()
        print("Taxi is moving...")

        # Journey control loop
        while taxi.is_running:
            print("\nSelect an option:")
            print("1. Move (Keep Moving)")
            print("2. Stop (Wait)")
            print("3. Arrive (Finish)")

            choice = input("> ").strip()

            if choice == "1":
                if taxi.current_state != "1":
                    taxi.change_state()
                    print("Taxi is now moving.")
                else:
                    print("Still moving...")

            elif choice == "2":
                if taxi.current_state != "2":
                    taxi.change_state()
                    print("Taxi stopped (waiting).")
                else:
                    print("Still stopped...")

            elif choice == "3":
                final_fare = taxi.stop_journey()
                print("\n----- TRIP FINISHED -----")
                print(f"Total fare is € {final_fare:.2f}")

                history_mgr.save_trip(customer_name, final_fare)
                break

            else:
                print("Invalid option. Try 1, 2, or 3.")

        # Exit confirmation
        quit_ans = input(
            f"\n{customer_name}, do you want to exit program? (Y/N) > "
        ).strip().upper()

        if quit_ans == "Y":
            print("Thank you. Goodbye!")
            break


if __name__ == "__main__":
    main()
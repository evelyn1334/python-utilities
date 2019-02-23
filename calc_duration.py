#!/usr/bin/env python3
"""
A simple CLI utility to calculate the duration between two points in time.
"""

import sys
from datetime import datetime

OPTIONS ="""\
1. How much time has elapsed since that point in time?
2. How long to go until that point in time?
3. Calculate the duration between two points in time.
4. Refresh current time.
5. Exit the program."""
ERROR = "Please enter a valid option or format your strings correctly!"

def exec_option(option, now):
    """
    Execute the selected option, duh!
    """
    if option == 1 or option == 2:
        return input_time(now)
    elif option == 3:
        print("\nPlease enter two sets of date and time...")
        time_sets = []
        for i in range(2):
            print("\n-- Now for set {0} --".format(i + 1))
            time_sets.append(input_time(now))
        return time_sets
    elif option == 4:
        print() # Print a blank line.
        main()
    elif option == 5:
        print("\nSee ya!\n")
        sys.exit()
    elif option not in range(1, 6):
        print("\n" + ERROR.upper() + "\n")
        main()

def input_time(now):
    """
    Let user enter date/time according to the specified formats.
    """
    print("\n<TIP> Hit Enter directly to use current date or time.")
    date_str = input("Enter a date in the format of YYYY-mm-DD : ").strip()
    time_str = input("Enter a time in the format of HH:MM:SS : ").strip()
    if not date_str and not time_str:
        print("\nPlease enter something! Let's start over...\n")
        main()
    elif not date_str:
        date_str = str(now.date())
    elif not time_str:
        time_str = str(now.time())
    datetime_str = date_str + " " + time_str
    time_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    return time_obj

def calc_duration(time_obj, now, option):
    """
    Calculate the duration between two points in time
    and return it as a timedelta object.
    """
    if type(time_obj) == list:
        if bool(time_obj[0] > time_obj[1]):
            duration = str(time_obj[0] - time_obj[1])
        else:
            duration = str(time_obj[1] - time_obj[0])
    else:
        if option == 1:
            if bool(now > time_obj):
                duration = str(now - time_obj)
            else:
                print("\nYou entered a future date or time! Let's start over...\n")
                main()
        elif option == 2:
            if bool(time_obj > now):
                duration = str(time_obj - now)
            else:
                print("\nYou entered a past date or time! Let's start over...\n")
                main()
    return duration

def print_result(option, duration):
    """
    Print out the calculated result in proper contexts.
    """
    if option == 1:
        print("\n*** " + duration + " has elapsed. ***\n")
    elif option == 2:
        print("\n*** There's still " + duration + " to go. ***\n")
    elif option == 3:
        print("\n*** The total duration is " + duration + " ***\n")

def main():
    """
    Main interface with some error handling. Also updates current time.
    """
    while True:
        x = datetime.now()
        # Rebuild current time, removing info about microsecond.
        now = datetime(x.year, x.month, x.day, x.hour, x.minute, x.second)
        print("\nCurrent time is " + str(now))
        print("\n" + OPTIONS)
        try:
            option = int(input("\nSelect an option to proceed: ").strip())
            time_obj = exec_option(option, now)
            duration = calc_duration(time_obj, now, option)
            print_result(option, duration)
        except ValueError:
            print("\n" + ERROR.upper() + "\n")
            continue


if __name__ == "__main__":
    main()

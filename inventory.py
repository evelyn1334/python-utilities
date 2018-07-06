#!/usr/bin/env python3
"""
A simple program to manage a personal inventory of medications.
Witten by Evelyn Huang in June 2018.
"""

import os, json, sys
from datetime import datetime

JSON_FNAME = ".inventory.json"
LOG_FNAME = ".inventory.log"
ABBRVS = ("cr", "er", "ir", "sr", "xl")
SEP_LINE = "-" * 50
RESTART_MSG = "Let's start over from the main menu..."
OPTIONS = """\
1. DISPLAY everything in the inventory.
2. TAKE a medication from the inventory.
3. ADD a medication to the inventory.
4. RENAME a medication in the inventory.
5. VIEW recent log entries.
6. EXIT the program."""

class Inventory:
    """
    A class with basic methods essential to manage a personal inventory of medications.
    """
    def __init__(self):
        """
        Initialize an inventory and creates/loads from the file where data is saved.
        """
        self.fpath = os.environ["HOME"] + "/" + JSON_FNAME
        self.current_meds = {}
        try:
            with open(self.fpath, "r") as f:
                self.current_meds = json.load(f)
        except FileNotFoundError:
            with open(self.fpath, "w") as f:
                json.dump({}, f)

    def display_everything(self):
        """
        Print out all of the medications in the inventory and their respective amounts.
        """
        meds = sorted(self.current_meds.keys())
        for med in meds:
            if med[-3] == " " and med[-2::] in ABBRVS:
                print(med[0:-3].capitalize(), med[-2::].upper() + ":", self.current_meds[med], "MG")
            else:
                print(med.capitalize() + ":", self.current_meds[med], "MG")

    def take_medication(self, med, dose):
        """
        Subtract from the current total dose. Remove the med if the total dose falls to 0.
        """
        self.current_meds[med] -= dose
        if self.current_meds[med] <= 0:
            del self.current_meds[med]

    def add_medication(self, med, dose):
        """
        Add to the current total dose. If med didn't exist, create an entry with the default dose set to 0.
        """
        self.current_meds[med] = self.current_meds.get(med, 0) + dose

    def rename_medication(self, med, new_name):
        """
        Create a new item with a new key and the same value while deleting the old one.
        """
        self.current_meds[new_name] = self.current_meds.pop(med)

    def finalize_changes(self):
        """
        Save changes to the json file.
        """
        with open(self.fpath, "w") as f:
            json.dump(self.current_meds, f)


def select_from_menu():
    """
    Print the options and retrieves the option given by the user.
    """
    error_msg = "Please enter a valid option!"
    print("\n" + OPTIONS + "\n")
    while True:
        option = input("Select an option to proceed: ")
        try:
            option = int(option)
            if option not in list(range(1, 7)):
                print("\n" + error_msg + "\n")
            else:
                return option
        except ValueError:
            print("\n" + error_msg + "\n")

def enter_medication(inventory, action, pass2=False):
    """
    An interface to enter or rename a medication with some restriction
    on the acceptable lengths of names.
    """
    while True:
        if not pass2:
            med = input("Enter the NAME of the medication: ").lower().strip()
        else:
            med = input("Enter the NEW NAME of the medication: ").lower().strip()
        if not med:
            print("\n" + RESTART_MSG)
            main(inventory)
        elif not pass2 and (med not in inventory.current_meds and action != "add"):
            print("\nThere is no such medication in your inventory!\n")
        elif len(med) < 3 or len(med) >= 40:
            print("\nThe medication name should be between 3 to 40 characters long!\n")
        else:
            return med

def enter_dose(inventory):
    """
    An interface to enter the dose with some built-in error-checking.
    """
    while True:
        dose = input("Enter the DOSE of the medication: ")
        if not dose:
            print("\n" + RESTART_MSG)
            main(inventory)
        try:
            return round(float(dose), 1)
        except ValueError:
            print("\nPlease enter a number expressed in Arabic numerals!\n")

def compose_msg(current_meds, med, new_name=None):
    """
    Compose messages for different scenarios after an action is performed.
    """
    done_msg1 = "Done!\nNow you have no {0} left in the inventory."
    done_msg2 = "Done!\nNow you have {0} MG of {1} in the inventory."
    done_msg3 = "Done!\n{0} has now been renamed {1}."
    if med not in current_meds and not new_name:
        return done_msg1.format(med.upper())
    elif med in current_meds and not new_name:
        return done_msg2.format(current_meds[med], med.upper())
    elif med not in current_meds and new_name in current_meds:
        return done_msg3.format(med.upper(), new_name.upper())

def log_action(action, med, dose=0, new_name=None):
    """
    Log the details of each action taken and saves them in a plain text file.
    """
    entry1 = "[{0}] {1} {2} to {3}.\n"
    entry2 = "[{0}] {1} {2} MG of {3}.\n"
    local_time = str(datetime.now()).split(".")[0]
    log_path = os.environ["HOME"] + "/" + LOG_FNAME
    if action == "take":
        action = "took"
    elif action == "add":
        action = "added"
    elif action == "rename":
        action = "renamed"
    try:
        logf = open(log_path, "a")
    except FileNotFoundError:
        logf = open(log_path, "w")
    if new_name:
        logf.write(entry1.format(local_time, action.capitalize(), med.upper(), new_name.upper()))
    else:
        logf.write(entry2.format(local_time, action.capitalize(), dose, med.upper()))
    logf.close()

def view_recent_log(inventory):
    """
    Print out the latest 10 entires from the log file.
    """
    log_path = os.environ["HOME"] + "/" + LOG_FNAME
    try:
        with open(log_path, "r") as logf:
            log_entries = logf.readlines()
            recent_entries = [entry for index, entry in enumerate(log_entries)
                              if len(log_entries) - index <= 10]
            print("\n" + SEP_LINE)
            for entry in recent_entries:
                print(entry.strip("\n"))
            print(SEP_LINE)
    except FileNotFoundError:
        print("\nNothing has been logged yet!")
        print("\n" + RESTART_MSG)
        main(inventory)

def modify_inventory(inventory, action):
    """
    Make changes to the inventory according to the action specified.
    """
    med = enter_medication(inventory, action)
    if action == "rename":
        new_name = enter_medication(inventory, action, pass2=True)
    else:
        dose = enter_dose(inventory)
    if action == "take":
        inventory.take_medication(med, dose)
        print("\n" + compose_msg(inventory.current_meds, med))
    elif action == "add":
        inventory.add_medication(med, dose)
        print("\n" + compose_msg(inventory.current_meds, med))
    elif action == "rename":
        inventory.rename_medication(med, new_name)
        print("\n" + compose_msg(inventory.current_meds, med, new_name=new_name))
    inventory.finalize_changes()
    if action == "rename":
        log_action(action, med, new_name=new_name)
    else:
        log_action(action, med, dose=dose)

def main(inventory):
    """
    Main interface to navigate through the system
    """
    while True:
        option = select_from_menu()
        if option == 1:
            if not inventory.current_meds:
                print("\nThere is nothing in your inventory!\n")
            else:
                print("\n" + SEP_LINE)
                inventory.display_everything()
                print(SEP_LINE)
        elif option == 2:
            modify_inventory(inventory, "take")
        elif option == 3:
            modify_inventory(inventory, "add")
        elif option == 4:
            modify_inventory(inventory, "rename")
        elif option == 5:
            view_recent_log(inventory)
        elif option == 6:
            print("\nSee you soon...\n")
            sys.exit()


if __name__ == "__main__":
    main(Inventory())

#!/usr/bin/env python3
"""
A simple CLI contact book.
"""

import sys
import json
import os

FILENAME = ".contacts.json"
OPTIONS = """\
1. Add an entry
2. Delete an entry
3. Display an entry
4. Display all entries
5. Display all aliases
6. Quit the program"""

class Contacts:

    def __init__(self):
        self.lst = []
        self.fpath = os.environ["HOME"] + "/" + FILENAME
        try:
            with open(self.fpath, "r") as f:
                self.lst = json.load(f)
        except FileNotFoundError:
            with open(self.fpath, "w") as f:
                json.dump([], f)

    def add_entry(self, alias, name, phone, address, email):
        entry = {alias: {"name": name, "phone": phone, "address": address, "email": email}}
        self.lst.append(entry)
        with open(self.fpath, "w") as f:
            json.dump(self.lst, f)

    def delete_entry(self, alias):
        for dct in self.lst[:]:
            if alias in dct:
                self.lst.remove(dct)
        with open(self.fpath, "w") as f:
            json.dump(self.lst, f)

    def display_entry(self, alias):
        for dct in self.lst:
            for als, content in dct.items():
                if als == alias:
                    print("\n<" + alias + ">")
                    for key, val in content.items():
                       print(key.capitalize() + ":", val)
                    print()

    def display_all(self):
        for dct in self.lst:
            for alias, content in dct.items():
                print("\n<" + alias + ">")
                for key, val in content.items():
                    print(key.capitalize() + ":", val)
                print("-" * 40)

    def display_aliases(self):
        print()
        for dct in self.lst:
            for key in dct.keys():
                print(key, end=" ", flush=True)
        print("\n" + "-" * 40 + "\n")

def check_input(contacts, option):
    while True:
        alias = input("Enter an alias: ")
        if not alias:
            print("Alias is required!")
            main(contacts)
        exists = False
        for dct in contacts.lst:
            if alias in dct:
                exists = True
        if option == 1:
            if exists:
                print("Alias already exists!")
                continue
            else:
                break
        elif option == 2:
            if exists:
                break
            else:
                print("There's no such entry!")
                continue
    return alias

def main(contacts):
    while True:
        print(OPTIONS)
        option = input("Select an option: ")
        if option.isnumeric():
            option = int(option)
            if option == 1:
                alias = check_input(contacts, option)
                name = input("Name: ")
                phone = input("Phone: ")
                address = input("Address: ")
                email = input("Email: ")
                contacts.add_entry(alias, name, phone, address, email)
                print("Added an entry\n")
            elif option == 2:
                alias =  check_input(contacts, option)
                contacts.delete_entry(alias)
                print("Deleted an entry\n")
            elif option == 3:
                alias = input("Enter an alias: ")
                contacts.display_entry(alias)
            elif option == 4:
                contacts.display_all()
            elif option == 5:
                contacts.display_aliases()
            elif option == 6:
                sys.exit()
        else:
            print("Please enter a valid option!\n")

if __name__ == "__main__":
    main(Contacts())

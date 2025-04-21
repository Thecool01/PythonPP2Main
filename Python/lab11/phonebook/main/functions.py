import psycopg2
from config import load_config
from db_functions import *

def functions_interface():
    while True:
        print('')
        print("---Functions---")

        print("1. Find contact by name and surname or phone")
        print("2. Insert new contact")
        print("3. Insert many contacts")
        print("4. Contacts in lists")
        print("5. Delete contact(by name or phone)")
        print("0. Back")
        choice = input("-> ")

        if choice == '1':
            pattern = input("Enter the name and surname or phone -> ")
            find_contacts(pattern)
        elif choice == '2':
            name = input('Enter the name -> ')
            phone = input('Enter the phone -> ')
            insert_user(name, phone)
        elif choice == '3':
            names = []
            phones = []
            n_names = int(input("Enter the number of names -> "))

            for _ in range(n_names):
                name = input(f"Enter the name {_} -> ")
                phone = input(f"Enter the phone for {name} -> ")
                names.append(name)
                phones.append(phone)

            insert_users(names, phones)

        elif choice == '4':
            limit = int(input("Enter limit for page -> "))
            pages = count_of_pages(limit)
            print(f"We have {pages} pages.")
            stop = False
            while not stop:
                print(f"Enter the page to show. From 1 to {pages}")
                page = int(input("(or 0 to EXIT)-> "))
                if page == 0:
                    break
                else:
                    show_page(limit, page)
        
        elif choice == '5':
            print("By name or phone?")
            choice1 = input("-> ")
            if choice1 == 'name':
                print("Enter the name to delete contact")
                name = input("-> ")
                delete_byname(name)
            elif choice1 == 'phone':
                print("Enter the phone number")
                phone = input("-> ")
                delete_byphone(phone)

        elif choice == '0':
            break

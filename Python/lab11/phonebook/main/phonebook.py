import time
import tabulate
from db_commands import * 

def interface():
    # Launching
    print("PhoneBook 1.0")
    time.sleep(0.3)
    print("Launching", end='', flush=True)
    for _ in range(3): print(".", end='', flush=True); time.sleep(0.3)

    print('')
    while True:
        print("PhoneBook 1.0")
        print("1. | Show all contacts |")
        print("2. | Show contacts using order |")        
        print("3. | Insert contact using console |")
        print("4. | Insert contact using csv |")
        print("5. | Update the contact using name |")        
        print("6. | Delete the contact using name or phone |")
        print("0. | Quit the program |")
        choice = int(input("Enter the number of the command -> "))

        if choice == 1:
            get_contacts()

        elif choice == 2:
            print("Select the filter to order")
            print("-> name")
            print("-> phone")
            
            order = input("-> ")

            get_contacs_with_order(order)

        elif choice == 3:
            name = input("Enter the name -> ")
            phone = int(input("Enter the phone number(max 20) -> "))

            insert_new_contact(name, phone)

        elif choice == 4:
            path = input(r"Enter the path for the file -> ")

            insert_new_from_csv(path)

        elif choice == 5:
            print("Enter the type to be changed(name | phone)")
            type = input("-> ")

            if type == "name":
                print("Enter the name to be changed")
                name = input("-> ")
                print("Enter a new name")
                new_name = input("-> ")

                update_name(name, new_name)
            
            elif type == "phone":
                print("Enter the name for which the phone will be changed")
                name = input("-> ")
                print("Enter a new phone")
                new_phone = input("-> ")

                update_phone(name, new_phone)
                
        elif choice == 6:
            part = input("Enter the type of the information(name | phone) -> ")
            value = input("Enter the value of the type -> ")

            delete_part(part, value)
            

        elif choice == 0:
            print("Goodbye!")
            time.sleep(0.2)
            return 0
        
interface()
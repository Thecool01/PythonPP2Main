import psycopg2
import csv
import time
from tabulate import tabulate

from config import load_config

def get_contacts():

    config = load_config()
    sql = """ SELECT name, phone FROM contacts;"""

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                print("The number of parts: ", cur.rowcount)
                rows = cur.fetchall()

                if not rows:
                    print("No contacts found!")
                    return

                headers = ["Name", "Phone"]
                print(tabulate(rows, headers=headers, tablefmt="psql")) # Use tabulate function
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_new_contact(name, phone):
    
    sql = f"""INSERT INTO contacts(name, phone)
             VALUES (%s, %s)"""
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (name, phone,))

                # Commit changes
                conn.commit()

                print("Please wait", end='', flush=True)

                for _ in range(3): print(".", end='', flush=True); time.sleep(0.3)
                print("\nInformation was successully added!")
                time.sleep(0.3)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_new_from_csv(path):

    with open(path, 'r', encoding='utf-8') as filecsv:
        reader = csv.reader(filecsv)
        data = list(reader)

        if not data:
            print("CSV is empty!")
            return 0
        
    
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                sql = f"INSERT INTO contacts (name, phone) VALUES (%s, %s)"

                cur.executemany(sql, data)
                conn.commit()
                
                time.sleep(0.3)
                print("The information was successfully added!")
                time.sleep(0.3)

                return len(data)
            
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def update_name(name, new_name):

    sql = f""" UPDATE contacts SET name='{new_name}'
                WHERE name='{name}' """


    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:

                cur.execute(sql)
                print(f"Name {name} was successfully changed to {new_name}!")

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def update_phone(name, new_phone):

    sql = f""" UPDATE contacts SET phone='{new_phone}'
                WHERE name='{name}' """


    config = load_config()

    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:

                # execute the UPDATE statement
                cur.execute(sql)
                print(f"Phone of {name} was successfully changed to {new_phone}!")

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)        

def get_contacs_with_order(order):

    config = load_config()

    if order == "name":

        sql = """ SELECT name, phone FROM contacts
                  ORDER BY name"""
        print("The phonebook with order by name\n")
    elif order == "phone":

        sql = """ SELECT name, phone FROM contacts
                  ORDER BY phone"""
        print("The phonebook with order by phone\n")

    else:
        
        print("Wrong filter!")
        return 0

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                print("The number of parts: ", cur.rowcount)
                rows = cur.fetchall()

                if not rows:
                    print("No contacts found!")
                    return 0
                

                headers = ["Name", "Phone"]
                print(tabulate(rows, headers=headers, tablefmt="psql"))
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def delete_part(part, value):
    """ Delete part by part id """

    if part == "name":
        sql = f"""DELETE FROM contacts WHERE name='{value}';"""

        print(f"The {value} in name was deleted")
    elif part == "phone":
        sql = f"""DELETE FROM contacts WHERE phone='{value}';"""
        
        print(f"The {value} in phone was deleted")
    
    else:
        print("Wrong part!")
        return 0 
    
    rows_deleted = 0
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # execute the UPDATE statement
                cur.execute(sql)
                rows_deleted = cur.rowcount

            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return rows_deleted

import psycopg2
from tabulate import tabulate
from config import load_config

def find_contacts(pattern):
    
    sql = f"""SELECT * FROM search_contacts('{pattern}');"""
    
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute(sql)
                rows = cur.fetchall()

                if not rows:
                    print("No contacts found!")
                    return

                headers = ["Name", "Phone"]
                print(tabulate(rows, headers=headers, tablefmt="psql")) # Use tabulate function
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_user(name, phone):
    
    sql = f"CALL upsert_user('{name}', '{phone}')"

    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute(sql)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_users(names, phones):
    
    sql = f"""
            CALL insert_multiple_users(
                %s::VARCHAR[], 
                %s::VARCHAR[], 
                'invalid_records'
            )
        """
    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute(sql, (names, phones))

                cur.execute("FETCH ALL FROM invalid_records")
                invalid_records = cur.fetchall()

                # Формируем отчет
                valid_count = len(names) - len(invalid_records)
                print(f"Success: {valid_count} records")
                print(f"Errors found: {len(invalid_records)}")

                if invalid_records:
                    print("\nWrong records")
                    for record in invalid_records:
                        name, phone, error = record
                        print(f"Имя: {name}, Телефон: {phone}, Ошибка: {error}")

            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def show_page(limit, page_number):
    
    total_pages = count_of_pages(limit)
    if page_number > total_pages or page_number < 1:
        print("Недопустимый номер страницы.")
        return

    sql = f"SELECT * FROM get_contacts_page({limit}, {page_number})"

    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute(sql)
                rows = cur.fetchall()

                headers = ["Name", "Phone"]
                print(tabulate(rows, headers=headers, tablefmt="psql"))

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def count_of_pages(limit):
    sql = f"SELECT CEIL(COUNT(*)::DECIMAL / %s) AS total_pages FROM contacts;"

    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute(sql, (limit,))
                result = cur.fetchone()
                total_pages = result[0]
                
                return total_pages
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None
    

def delete_byname(user_name):

    sql = f"CALL delete_user_byname('{user_name}')"

    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute(sql)
                print(f"Contact {user_name} was deleted!")
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def delete_byphone(user_phone):

    sql = f"CALL delete_user_byphone('{user_phone}')"

    config = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:

                cur.execute(sql)
                print(f"Contact with phone {user_phone} was deleted!")
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
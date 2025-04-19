import psycopg2
import sys
import os

from tabulate import tabulate
# For the import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import load_config

def get_player_data(nickname):

    config = load_config()
    sql = f"""
            SELECT nickname, score, level, snake_size, last_score 
            FROM snake_records 
            WHERE nickname='{nickname}'
            ORDER BY score DESC
            LIMIT 1
        """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                
                return cur.fetchone()

                
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def create_new_player(nickname):

    config = load_config()
    sql = """ INSERT INTO snake_records (nickname, score, level, snake_size, last_score)
            VALUES (%s, 0, 1, 1, 0) RETURNING nickname """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (nickname,))
                conn.commit()
                if cur.fetchone():
                    print(f"New player {nickname} created successfully!")
                    return True
                else:
                    return False

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False


def save_records(nickname, score, level, snake_size, last_score):

    config = load_config()
    sql = """ UPDATE snake_records 
              SET score=%s, level=%s, snake_size=%s, last_score=%s
              WHERE nickname=%s
              RETURNING nickname
            """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (score, level, snake_size, last_score, nickname))
                if cur.fetchone():
                    conn.commit()
                    print(f"Saving...")
                    return True
                else:
                    print ("No player found to update")
                    return False

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False

def init_player():

    print("Welcome to the Snake Game!")
    print("Enter your nickname")
    nickname = input("-> ")

    player_data = get_player_data(nickname)

    if player_data:
        print(f"Welcome back, {nickname}!")
        print(f"Your best score: {player_data[1]} and level:{player_data[2]}")

        return player_data[0], player_data[1], player_data[2], player_data[3], player_data[4]
    else:
        print(f"Welcome new player {nickname}!")
        print(f"Your data was saved!")
        create_new_player(nickname)
        return nickname, 0, 1, 1, 0


def list_information(nickname):

    config = load_config()
    sql = """ SELECT nickname, score, level FROM snake_records
                WHERE nickname=%s;
            """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (nickname,))
                rows = cur.fetchall()

                if not rows:
                    print("No players found!")
                    return

                headers = ["Nickname", "Best score", "Level"]
                print(tabulate(rows, headers=headers, tablefmt="psql")) # Use tabulate function

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False


def top_players():

    config = load_config()
    sql = """ SELECT nickname, score, level FROM snake_records
                ORDER BY score DESC 
                LIMIT 10;
            """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()

                if not rows:
                    print("No players found!")
                    return

                headers = ["Nickname", "Best score", "Level"]
                print("Top 10 of players")
                print(tabulate(rows, headers=headers, tablefmt="psql")) # Use tabulate function

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
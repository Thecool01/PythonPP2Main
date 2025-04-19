import psycopg2
import sys
import os
# For the import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import load_config

def get_player_data(nickname):

    config = load_config()
    sql = f"""
            SELECT nickname, score, level 
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
    sql = """ INSERT INTO snake_records (nickname, score, level)
            VALUES (%s, 0, 1) """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (nickname,))
                print(f"New player {nickname} was created!")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def save_records(nickname, score, level):

    config = load_config()
    sql1 = f""" UPDATE snake_records SET score='{score}'
                WHERE nickname='{nickname}' """

    sql2 = f""" UPDATE snake_records SET level='{level}'
                WHERE nickname='{nickname}' """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql1)
                cur.execute(sql2)
                print(f"The best results was saved!")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def init_player():

    print("Welcome to the Snake Game!")
    print("Enter your nickname")
    nickname = input("-> ")

    player_data = get_player_data(nickname)

    if player_data:
        print(f"Welcome back, {nickname}!")
        print(f"Your best score: {player_data[1]} and level:{player_data[2]}")

        return player_data[0], player_data[1], player_data[2]
    else:
        print(f"Welcome new player {nickname}!")
        print(f"Your data was saved!")
        new_player = create_new_player(nickname)
        if new_player:
            return new_player[0], new_player[1], new_player[2]

    # In case of an error, we simply send the standard data.
    return nickname, 0, 1 


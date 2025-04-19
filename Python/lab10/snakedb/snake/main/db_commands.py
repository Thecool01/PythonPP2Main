import psycopg2
import sys
import os
# For the import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import load_config

def get_player_data(nickname):

    config = load_config()
    sql = f"""
            SELECT nickname, score, level, snake_size 
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
    sql = """ INSERT INTO snake_records (nickname, score, level, snake_size)
            VALUES (%s, 0, 1, 1) """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (nickname,))
                print(f"New player {nickname} was created!")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def save_records(nickname, score, level, snake_size):

    config = load_config()
    sql = """ UPDATE snake_records 
              SET score=%s, level=%s, snake_size=%s
              WHERE nickname=%s
              RETURNING nickname
            """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (score, level, snake_size, nickname))
                if cur.fetchone():
                    conn.commit()
                    print(f"The best results was saved!")
                    return True
                else:
                    print ("No player found to update")
                    return False

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False


def save_records_gameover(nickname, score, level):

    config = load_config()
    sql = """ UPDATE snake_records 
              SET score=%s, level=%s
              WHERE nickname=%s
              RETURNING nickname
            """

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (score, level, nickname))
                if cur.fetchone():
                    conn.commit()
                    print(f"The best results was saved!")
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

        return player_data[0], player_data[1], player_data[2], player_data[3]
    else:
        print(f"Welcome new player {nickname}!")
        print(f"Your data was saved!")
        create_new_player(nickname)
        return nickname, 0, 1, 1

    # In case of an error, we simply send the standard data.


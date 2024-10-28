import os

import psycopg2
import datetime
import scr.func

HOST = os.environ.get("HOST", default="localhost")
DBNAME = os.environ.get("DBNAME", default="Vodokanal")
PASSWORD = os.environ.get("PASSWORD", default="nikita041216")
USER = os.environ.get("USER", default="postgres")
PORT = os.environ.get("PORT", default="5432")


def select_address_to_choice():
    try:
        conn = psycopg2.connect(
            dbname=DBNAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        cursor = conn.cursor()

        cursor.execute(f""" SELECT * FROM show_address_data_to_choice() """)
        data = cursor.fetchall()

        cursor.close()
        conn.close()
        return data
    except Exception as ex:
        print(ex)


def select_employer_to_choice():
    try:
        conn = psycopg2.connect(
            dbname=DBNAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        cursor = conn.cursor()

        cursor.execute(f""" SELECT * FROM get_list_employer() """)
        data = cursor.fetchall()

        cursor.close()
        conn.close()
        return data
    except Exception as ex:
        print(ex)

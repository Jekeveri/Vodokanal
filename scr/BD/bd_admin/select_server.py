import psycopg2
import datetime
import scr.func


def select_address_to_choice():
    try:
        conn = psycopg2.connect(
            dbname="test",
            user="postgres",
            password='123321'
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
            dbname="test",
            user="postgres",
            password='123321'
        )
        cursor = conn.cursor()

        cursor.execute(f""" SELECT * FROM get_list_employer() """)
        data = cursor.fetchall()

        cursor.close()
        conn.close()
        return data
    except Exception as ex:
        print(ex)

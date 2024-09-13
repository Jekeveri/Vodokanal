import psycopg2
import datetime

import scr.BD.bd_users.select_bd
import scr.BD.bd_users.insert_bd
import scr.BD.bd_users.create_bd
import scr.BD.bd_users.update_bd
import scr.func
import scr.navigation_apps.navigations


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
        # if data:
        #     for record in data:
        #         address_id, city, district, street, dom, apartment, entrance = record

        cursor.close()
        conn.close()
        return data
    except Exception as ex:
        print(ex)

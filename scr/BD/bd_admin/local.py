import sqlite3 as sl
import scr.navigation_apps.navigations


def local_user_db():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        table_user = """ Create table if not exists user
        (id Integer, login Text, password Text, privileges integer, first_name Text, last_name Text) """
        cursor.execute(table_user)


def insert_bd_user(id_user, login, password, privileges, first_name, last_name, page):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into user values({id_user}, '{login}', '{password}', 
                    {privileges}, '{first_name}','{last_name}' ) """
        cursor.execute(query)
    scr.navigation_apps.navigations.role_definition(privileges, page)


def delete_data_db():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        delete_user = """ Delete from user """
        cursor.execute(delete_user)


def select_user_data():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """ Select id, login, password, privileges, last_name, first_name from user """
        cursor.execute(query)
        result = cursor.fetchall()
        return result

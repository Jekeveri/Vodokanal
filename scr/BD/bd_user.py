import os
import sqlite3 as sl

import scr.navigation_apps.navigations


def local_user_db():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        table_task = """ Create table if not exists tasks(id Integer, client_data Text, meters_data Text,last_reading Text, 
        date Text,status Text, remark Text) """
        table_picture = """ Create table if not exists picture(id Integer, value BLOB, task_id Integer) """
        table_user = """ Create table if not exists user(id Integer, login Text, password Text, privileges integer) """
        cursor.execute(table_task)
        cursor.execute(table_picture)
        cursor.execute(table_user)


def insert_bd_user(id_user, login, password, privileges, page):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into user values({id_user}, {login}, {password}, {privileges}) """
        cursor.execute(query)
    scr.navigation_apps.navigations.role_definition(privileges, page)


def select_user_data():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """ Select login, password, privileges from user """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def delete_data_db():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """ Delete from user """
        cursor.execute(query)
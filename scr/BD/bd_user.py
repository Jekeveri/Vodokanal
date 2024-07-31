import os
import sqlite3 as sl

import scr.navigation_apps.navigations


def local_user_db():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        table_task = """ Create table if not exists tasks(id Integer, name Text, address_id integer, phone_number Text, 
        email Text, meters_number Text, instalation_day Text, meter_type Text, 
        last_reading_date Text, last_reading_value Text, date Text, remark Text, status Text ) """
        table_picture = """ Create table if not exists picture(id Integer, value BLOB, task_id Integer) """
        table_user = """ Create table if not exists user(id Integer, login Text, password Text, privileges integer) """
        table_address = """ Create table if not exists address(id integer, city text, district text, street Text, 
        dom text, floor text, entrance text)"""
        cursor.execute(table_task)
        cursor.execute(table_picture)
        cursor.execute(table_user)
        cursor.execute(table_address)


def insert_bd_user(id_user, login, password, privileges, page):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into user values({id_user}, {login}, {password}, {privileges}) """
        cursor.execute(query)
    scr.BD.bd_server.select_task_data(id_user)
    scr.navigation_apps.navigations.role_definition(privileges, page)


def insert_bd_task(task_id, name, address_id, city, district, street, dom, floor, entrance, phone_number, email,
                   meter_number, instalation_day,
                   meter_type, last_reading_date, reading_value, date_task, remark, status_task):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into tasks values ({task_id}, '{name}', {address_id}, '{phone_number}', '{email}', 
            '{meter_number}', '{instalation_day}', '{meter_type}', '{last_reading_date}', 
            '{reading_value}', '{date_task}', '{remark}', '{status_task}')"""
        cursor.execute(query)
        query2 = f""" Insert into address values ({address_id},'{city}', '{district}', '{street}', '{dom}', '{floor}', '{entrance}')"""
        cursor.execute(query2)
        print(task_id)


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

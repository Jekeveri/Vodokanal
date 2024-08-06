import os
import sqlite3 as sl
import datetime

import scr.navigation_apps.navigations


def local_user_db():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        table_task = """ Create table if not exists tasks(id Integer, name Text, address_id integer, phone_number Text, 
        email Text, id_customer integer, date Text, remark Text, status Text, unloading_time Text ) """
        table_meters = """ Create table if not exists meters(
        id Integer, meter_number Text, instalation_date Text, meter_type text, id_customer integer)"""
        table_meter_reading = """ Create table if not exists meter_reading(
        meter_id integer, last_reading_date Text, last_reading_value Text) """
        table_picture = """ Create table if not exists picture(id Integer, value BLOB, task_id Integer) """
        table_user = """ Create table if not exists user(id Integer, login Text, password Text, privileges integer) """
        table_address = """ Create table if not exists address(id integer, city text, district text, street Text, 
        dom text, apartment text, entrance text)"""
        cursor.execute(table_task)
        cursor.execute(table_meters)
        cursor.execute(table_meter_reading)
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


def insert_bd_task(task_id, name, address_id, city, district, street, dom, apartment,
                   entrance, id_customer, phone_number, email, date_task, remark, status_task):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into tasks 
        (id, name, address_id, phone_number, email, id_customer, date, remark, status)
         values ({task_id}, '{name}', {address_id}, '{phone_number}', '{email}', 
            {id_customer}, '{date_task}', '{remark}', '{status_task}') """
        cursor.execute(query)
        query2 = f""" Insert into address values ({address_id},'{city}', '{district}', '{street}', '{dom}', 
            '{apartment}', '{entrance}')"""
        cursor.execute(query2)


def insert_bd_meters(id_meter, meter_number, instalation_day, meter_type, id_customer):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into meters 
        (id, meter_number, instalation_date, meter_type, id_customer)
         values ({id_meter}, '{meter_number}', {instalation_day}, '{meter_type}', {id_customer}) """
        cursor.execute(query)


def insert_bd_meter_reading(meter_id, reading_date, reading_values):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into meter_reading 
        (meter_id,last_reading_date, last_reading_value)
         values ({meter_id}, '{reading_date}', {reading_values}) """
        cursor.execute(query)


def select_user_data():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """ Select login, password, privileges from user """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def select_task_data():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """ Select t.id, a.street, a.dom, a.apartment, t.status from tasks as t
            join address as a on a.id = t.address_id """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def select_task_data_new():  # потом переделываем select_task_data здесь на другой
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """ Select t.id, t.name, a.street, a.dom, a.apartment, t.phone_number, 
        t.email, t.meter_id, t.meters_number, t.instalation_day, t.meter_type, 
        t.last_reading_date, t.last_reading_value, t.date, t.remark, t.status from tasks as t
            join address as a on a.id = t.address_id """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def delete_data_db():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        delete_user = """ Delete from user """
        delete_task = """ Delete from tasks """
        delete_address = """ Delete from address """
        delete_photo = """ Delete from picture """
        cursor.execute(delete_user)
        cursor.execute(delete_task)
        cursor.execute(delete_address)
        cursor.execute(delete_photo)


def update_local_tasks(unloading_time, task_id, reading_value, remark):
    with sl.connect('database_client.db') as db:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor = db.cursor()
        query = f""" update tasks set 
            unloading_time = '{unloading_time}',  
            remark = '{remark}',
            status = 'выполнен'
            where id = {task_id}"""
        cursor.execute(query)
        query1 = f""" update meter_reading set  
            last_reading_date = '{today}',
            last_reading_value = '{reading_value}'
            where meter_id = (select m.id from meters as m
            join tasks as t on m.id_customer = t.id_customer
            where m.id_customer =t.id_customer and t.id = {task_id}) """
        cursor.execute(query1)
        db.commit()


def get_data_to_upload():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """ Select t.id, t.unloading_time, mr.last_reading_value, 
        mr.last_reading_date, t.remark, t.status, mr.meter_id from tasks as t
        join meters as m on m.id_customer = t.id_customer
        join meter_reading as mr on mr.meter_id = m.id"""
        cursor.execute(query)
        result = cursor.fetchall()
        return result

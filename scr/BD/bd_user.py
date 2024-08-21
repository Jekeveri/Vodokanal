import os
import sqlite3 as sl
import datetime

import scr.navigation_apps.navigations


def local_user_db():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        table_task = """ Create table if not exists tasks(id Integer, name Text, id_address integer, phone_number Text, 
        personal_account Text, date Text, remark Text, status Text, unloading_time Text, purpose Text ) """
        table_meters = """ Create table if not exists meters(
        id Integer, meter_number Text, instalation_date Text, meter_type text, id_address integer,
        marka Text, seal_number Text, date_next_verification Text, location Text, saldo Text,
        status_filling Text, meter_remark Text) """
        table_meter_reading = """ Create table if not exists meter_reading(
        meter_id integer, last_reading_date Text, last_reading_value Text, 
        new_reading_date Text, new_reading_value Text) """
        table_picture = """ Create table if not exists picture(id Integer, value BLOB, task_id Integer) """
        table_user = """ Create table if not exists user
        (id Integer, login Text, password Text, privileges integer, first_name Text, last_name Text) """
        table_address = """ Create table if not exists address(id integer, city text, district text, street Text, 
        dom text, apartment text, entrance text, registered_residing integer, 
        status Text, standarts REAL, area REAL )"""
        cursor.execute(table_task)
        cursor.execute(table_meters)
        cursor.execute(table_meter_reading)
        cursor.execute(table_picture)
        cursor.execute(table_user)
        cursor.execute(table_address)


def insert_bd_user(id_user, login, password, privileges, first_name, last_name, page):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into user values({id_user}, '{login}', '{password}', 
            {privileges}, '{first_name}','{last_name}' ) """
        cursor.execute(query)
    scr.BD.bd_server.select_task_data(id_user)
    scr.navigation_apps.navigations.role_definition(privileges, page)


def insert_bd_task(task_id, name, address_id, city, district, street, dom, apartment,
                   entrance, phone_number, personal_account, date_task, remark, status_task, purpose,
                   registered_residing, address_status, standarts, area):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into tasks 
        (id, name, id_address, phone_number, personal_account, date, remark, status, purpose)
         values ({task_id}, '{name}', {address_id}, '{phone_number}', '{personal_account}', 
            '{date_task}', '{remark}', '{status_task}', '{purpose}') """
        cursor.execute(query)

        query2 = f""" Insert into address values ({address_id}, '{city}', '{district}', '{street}', '{dom}', 
            '{apartment}', '{entrance}', {registered_residing}, '{address_status}',  {standarts}, {area})"""
        cursor.execute(query2)


def insert_bd_meters(id_meter, meter_number, instalation_day, meter_type, id_address, meter_remark, marka, seal_number,
                     date_next_verification, location, saldo):
    if meter_remark is None:
        meter_remark = ""
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into meters 
        (id, meter_number, instalation_date, meter_type, id_address, status_filling, meter_remark,
        marka, seal_number, date_next_verification, location, saldo)
         values ({id_meter}, '{meter_number}', '{instalation_day}', '{meter_type}', 
            {id_address}, 'невыполнено', '{meter_remark}', '{marka}', '{seal_number}', 
            '{date_next_verification}', '{location}', {saldo})"""
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
        query = """ Select login, password, privileges, last_name, first_name from user """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def select_meters_data_new(id_task):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Select m.* from meters as m
          join tasks as t on t.id_address = m.id_address
          where t.id ={id_task} """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def select_meter_reading_new(meter_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Select meter_id, last_reading_date, last_reading_value, 
            new_reading_date, new_reading_value from meter_reading 
          where meter_id = {meter_id} """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def select_tasks_data_new():  # потом переделываем select_task_data здесь на другой
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """ Select t.id|| '', t.name, a.street, a.dom, a.apartment, t.phone_number, 
        t.personal_account || '', t.date, t.remark, t.status, t.purpose, a.registered_residing|| '', 
        a.status, a.standarts|| '', a.area|| '' from tasks as t
            join address as a on a.id = t.id_address """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def delete_data_db():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        delete_user = """ Delete from user """
        delete_task = """ Delete from tasks """
        delete_address = """ Delete from address """
        delete_meters = """ Delete from meters """
        delete_meter_reading = """ Delete from meter_reading """
        delete_photo = """ Delete from picture """
        cursor.execute(delete_user)
        cursor.execute(delete_meters)
        cursor.execute(delete_meter_reading)
        cursor.execute(delete_task)
        cursor.execute(delete_address)
        cursor.execute(delete_photo)


def update_local_tasks(unloading_time, task_id, reading_value, remark, meter_id):
    with sl.connect('database_client.db') as db:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor = db.cursor()
        query = f""" update tasks set 
            unloading_time = '{unloading_time}',  
            status = 'выполнен'
            where id = {task_id}"""
        cursor.execute(query)
        query1 = f""" update meter_reading set  
            new_reading_date = '{today}',
            new_reading_value = '{reading_value}'
            where meter_id = {meter_id} """
        query2 = f""" update meters set  
            status_filling = 'выполнен',
            meter_remark = '{remark}'
            where id = {meter_id} """
        cursor.execute(query1)
        cursor.execute(query2)
        db.commit()


def get_data_to_upload():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """ Select t.id, t.unloading_time, mr.new_reading_value, 
        mr.new_reading_date, t.remark, t.status, mr.meter_id from tasks as t
        join meters as m on m.id_address = t.id_address
        join meter_reading as mr on mr.meter_id = m.id"""
        cursor.execute(query)
        result = cursor.fetchall()
        return result

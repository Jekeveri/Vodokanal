import os
import sqlite3 as sl
import scr.navigation_apps.navigations


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
                   registered_residing, address_status, standarts, area, saldo, type_address):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into tasks 
        (id, name, id_address, phone_number, personal_account, date, remark, status, purpose, saldo)
         values ({task_id}, '{name}', {address_id}, '{phone_number}', '{personal_account}', 
            '{date_task}', '{remark}', '{status_task}', '{purpose}', {saldo}) """
        cursor.execute(query)

        query2 = f""" Insert into address values ({address_id}, '{city}', '{district}', '{street}', '{dom}', 
            '{apartment}', '{entrance}', {registered_residing}, '{address_status}',  {standarts}, {area}, '{type_address}')"""
        cursor.execute(query2)


def insert_bd_meters(id_meter, meter_number, instalation_day, meter_type, id_address, meter_remark, marka, seal_number,
                     date_next_verification, location):
    if meter_remark is None:
        meter_remark = ""
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into meters 
        (id, meter_number, instalation_date, meter_type, id_address, status_filling, meter_remark,
        marka, seal_number, date_next_verification, location)
         values ({id_meter}, '{meter_number}', '{instalation_day}', '{meter_type}', 
            {id_address}, 'невыполнено', '{meter_remark}', '{marka}', '{seal_number}', 
            '{date_next_verification}', '{location}')"""
        cursor.execute(query)


def insert_bd_meter_reading(id_meter_reading, meter_id, reading_date, reading_values):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Insert into meter_reading 
        (id, meter_id,last_reading_date, last_reading_value)
         values ({id_meter_reading},{meter_id}, '{reading_date}', {reading_values}) """
        cursor.execute(query)


def insert_photo(name_file, value, task_id, meter_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """INSERT INTO picture 
                   (name_file, value, task_id, meter_id) 
                   VALUES (?, ?, ?, ?)"""
        cursor.execute(query, (name_file, value, task_id, meter_id))
        db.commit()

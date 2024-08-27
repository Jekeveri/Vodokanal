import sqlite3 as sl


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
        a.status, a.standarts|| '', a.area|| '', t.saldo from tasks as t
            join address as a on a.id = t.id_address """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def select_tasks_data_for_one(id_task):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Select t.id|| '', t.name, a.street, a.dom, a.apartment, t.phone_number, 
        t.personal_account || '', t.date, t.remark, t.status, t.purpose, a.registered_residing|| '', 
        a.status, a.standarts|| '', a.area|| '', t.saldo from tasks as t
            join address as a on a.id = t.id_address 
            where t.id = {id_task} """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def select_meters_data_new_for_one(id_task, meter_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Select m.* from meters as m
          join tasks as t on t.id_address = m.id_address
          where t.id ={id_task} and m.id = {meter_id} """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


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

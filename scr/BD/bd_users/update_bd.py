import sqlite3 as sl
import datetime


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


def update_dop_data_address(remark, saldo, registered_residing, standarts, area, address_id, task_id, id_meters):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" update tasks set 
            remark = '{remark}'  
            where id = {task_id}"""
        cursor.execute(query)
        query1 = f""" update address set  
            registered_residing = '{int(registered_residing)}',
            standarts = '{standarts}',
            area = '{area}'
            where id = {address_id} """
        # query2 = f""" update meters set
        #     saldo = {saldo},
        #     meter_remark = '{remark}'
        #     where id = {id_meters} """
        cursor.execute(query1)
        # cursor.execute(query2)
        db.commit()

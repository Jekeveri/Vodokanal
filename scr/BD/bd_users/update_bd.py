import sqlite3 as sl
import datetime


def update_local_tasks(unloading_time, task_id, reading_value, remark, meter_id):
    with sl.connect('database_client.db') as db:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        cursor = db.cursor()
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
        query = f""" update tasks set 
            unloading_time = '{unloading_time}',  
            status = 'выполнен'
            where id = {task_id} and id IN (
              SELECT DISTINCT t.id
              FROM tasks t
              JOIN address a ON t.id_address = a.id
              JOIN meters m ON a.id = m.id_address
              WHERE NOT EXISTS (
                SELECT 1
                FROM meters m2
                WHERE m2.id_address = a.id
                AND NOT EXISTS (
                  SELECT 1
                  FROM meter_reading mr
                  WHERE mr.meter_id = m2.id
                  AND mr.new_reading_value IS NOT NULL
                )
              )
            );"""
        cursor.execute(query)
        db.commit()


def update_dop_data_address(remark, registered_residing, standarts, area, address_id, task_id,):
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
        cursor.execute(query1)
        db.commit()

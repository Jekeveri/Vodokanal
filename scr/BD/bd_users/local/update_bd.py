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
                   status = 'в_исполнении'
                   where id = {task_id}"""
        cursor.execute(query)
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


def update_dop_data_address(remark, registered_residing, standarts, area, address_id, task_id, ):
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


def update_tasks_data_from_server(task_id, name, address_id, city, district, street, dom, apartment, entrance,
                                  registered_residing, address_status, standarts, area, phone_number,
                                  personal_account, date_task, remark, status_task, purpose, saldo):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" 
        insert into tasks (id, name,id_address, phone_number,
                            personal_account, date, remark, status, purpose, saldo)
        values
        ({task_id}, '{name}', {address_id}, '{phone_number}','{personal_account}', '{date_task}', '{remark}', 
        '{status_task}', '{purpose}', '{saldo}')
        on conflict(id) do update set
            name = '{name}',
            id_address = {address_id}, 
            phone_number = '{phone_number}',
            personal_account = '{personal_account}',
            date = '{date_task}',
            remark =' {remark}',
            status = '{status_task}',
            purpose = '{purpose}',
            saldo = '{saldo}'"""
        cursor.execute(query)
        db.commit()
        query = f""" 
                insert into address (id, city, district, street, dom, apartment, entrance, registered_residing, status, 
                                    standarts, area)
                values
                ('{address_id}', '{city}', '{district}', '{street}', '{dom}', '{apartment}', '{entrance}', 
                {registered_residing}, '{address_status}', {standarts}, {area})
                on conflict(id) do update set
                    city = '{city}', 
                    district = '{district}', 
                    street = '{street}', 
                    dom = '{dom}', 
                    apartment = '{apartment}', 
                    entrance = '{entrance}', 
                    registered_residing = {registered_residing}, 
                    status = '{address_status}', 
                    standarts = {standarts}, 
                    area = {area}"""
        cursor.execute(query)


def update_meter_data_from_server(id_meter, meter_number, instalation_day, meter_type, id_address, meter_remark,
                                  marka, seal_number, date_next_verification, location):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" 
        insert into meters (id, meter_number, instalation_date, meter_type, id_address,
        marka, seal_number, date_next_verification, location,
        meter_remark)
        values
        ({id_meter}, '{meter_number}', '{instalation_day}', '{meter_type}', {id_address}, '{marka}', '{seal_number}', 
        '{date_next_verification}', '{location}', '{meter_remark}')
        on conflict(id) do update set
            meter_number = '{meter_number}', 
            instalation_date = '{instalation_day}', 
            meter_type = '{meter_type}', 
            id_address = {id_address},
            marka = '{marka}', 
            seal_number = '{seal_number}', 
            date_next_verification = '{date_next_verification}', 
            location = '{location}',
            meter_remark = '{meter_remark}'"""
        cursor.execute(query)
        db.commit()


def update_meter_reading_data_from_server(id_meter_reading, meter_id, reading_date, reading_values):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" 
        insert into meter_reading (id, meter_id, last_reading_date, last_reading_value)
        values
        ({id_meter_reading}, {meter_id}, '{reading_date}', '{reading_values}')
        on conflict(id) do update set
            meter_id = {meter_id}, 
            last_reading_date = '{reading_date}', 
            last_reading_value = '{reading_values}' """
        cursor.execute(query)
        db.commit()


def update_seal(seal_number, meter_id, task_id, remark):
    with sl.connect('database_client.db') as db:
        today = datetime.datetime.now().strftime("%H:%M:%S")
        cursor = db.cursor()
        query2 = f""" update meters set  
                            status_filling = 'выполнен',
                            seal_number = '{seal_number}'
                            meter_remark = '{remark}'
                            where id = {meter_id} """
        cursor.execute(query2)
        db.commit()

        query = f""" update tasks set 
                           unloading_time = '{str(today)}',  
                           status = 'в_исполнении'
                           where id = {task_id}"""
        cursor.execute(query)
        db.commit()

        query = f""" update tasks set 
                            unloading_time = '{str(today)}',  
                            status = 'выполнен'
                            where id = {task_id} and id IN (
                              SELECT DISTINCT t.id
                              FROM tasks t
                              JOIN address a ON t.id_address = a.id
                              JOIN meters m ON a.id = m.id_address
                              WHERE m.status_filling = 'выполнен'
                            );
                  """
        cursor.execute(query)
        db.commit()


def update_date(id_task, date):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" update tasks set 
                           date = '{date}'  
                           where id = {id_task}"""
        cursor.execute(query)
        db.commit()

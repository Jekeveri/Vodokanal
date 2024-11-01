import sqlite3 as sl


def select_user_data():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """ Select id, login, password, privileges, last_name, first_name from user """
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


def select_tasks_data_new(sorting, search_value):
    search_value = search_value.lower()
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f"""Select t.id|| '', t.name, a.district, a.street, a.dom, a.apartment, t.phone_number, 
                    t.personal_account || '', t.date, t.remark, t.status, t.purpose, 
                    a.registered_residing '', a.status, a.standarts '', a.area|| '', t.saldo 
                    from tasks as t
                    join address as a on a.id = t.id_address
                    where t.date = current_date"""

        if sorting == "Адрес":
            query += f""" order by a.street, a.dom, a.apartment"""
        elif sorting == "Дата":
            query += f""" order by t.date"""
        else:
            query += f""" order by t.status"""

        cursor.execute(query)
        result = cursor.fetchall()

        filtered_result = [
            row for row in result if
            search_value in row[2].lower() or  # a.district
            search_value in row[3].lower() or  # a.street
            search_value in row[4].lower() or  # a.dom
            search_value in row[5].lower()  # a.apartment
        ]

        return filtered_result


def select_future_tasks_data_new(sorting, search_value):
    search_value = search_value.lower()
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f"""Select t.id|| '', t.name, a.district, a.street, a.dom, a.apartment, t.phone_number, 
                    t.personal_account || '', t.date, t.remark, t.status, t.purpose, 
                    a.registered_residing '', a.status, a.standarts '', a.area|| '', t.saldo 
                    from tasks as t
                    join address as a on a.id = t.id_address
                    where t.date > current_date"""

        if sorting == "Адрес":
            query += f""" order by a.street, a.dom, a.apartment"""
        elif sorting == "Дата":
            query += f""" order by t.date """
        else:
            query += f""" order by t.status"""

        cursor.execute(query)
        result = cursor.fetchall()

        filtered_result = [
            row for row in result if
            search_value in row[2].lower() or  # a.district
            search_value in row[3].lower() or  # a.street
            search_value in row[4].lower() or  # a.dom
            search_value in row[5].lower()  # a.apartment
        ]

        return filtered_result


def select_tasks_data_for_one(id_task):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" Select t.id|| '', t.name, a.street, a.dom, a.apartment, t.phone_number, 
        t.personal_account || '', t.date, t.remark, t.status, t.purpose, a.registered_residing|| '', 
        a.status, a.standarts|| '', a.area|| '', t.saldo, a.type_address from tasks as t
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
        mr.new_reading_date, t.remark, t.status, mr.meter_id, m.meter_remark, t.purpose, m.seal_number from tasks as t
        join meters as m on m.id_address = t.id_address
        join meter_reading as mr on mr.meter_id = m.id"""
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def select_photo_data_new(meter_id, task_id):
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = f""" select * from picture where meter_id = {meter_id} and task_id = {task_id} """
        cursor.execute(query)
        result = cursor.fetchall()
        return result


def get_dop_data_to_upload():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        query = """ Select a.id, a.registered_residing, a.status, a.standarts, a.area, t.remark, t.id from address as a
                    join tasks as t on t.id_address = a.id"""
        cursor.execute(query)
        result = cursor.fetchall()
        return result


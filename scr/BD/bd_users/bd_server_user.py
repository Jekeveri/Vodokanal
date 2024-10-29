import os

import datetime

import scr.BD.bd_users.local.select_bd
import scr.BD.bd_users.local.insert_bd
import scr.BD.bd_users.local.create_bd
import scr.BD.bd_users.local.update_bd
import scr.func
import scr.navigation_apps.navigations


def select_task_data(id_user):
    res = scr.BD.bd_users.local.select_bd.select_user_data()
    if res:
        for record in res:
            user_id, login, password, privileges, first_name, last_name = record
    conn = scr.func.get_user_db_connection(login, password)
    cursor = conn.cursor()

    cursor.execute(f""" SELECT * FROM get_task_data_new({id_user}) """)
    task_data = cursor.fetchall()

    if task_data:
        for record in task_data:
            task_id, name, address_id, city, district, street, dom, apartment, entrance, \
                registered_residing, address_status, standarts, area, phone_number, \
                personal_account, date_task, remark, status_task, purpose, saldo, type_address = record

            scr.BD.bd_users.local.insert_bd.insert_bd_task(
                task_id, name, address_id, city, district, street, dom, apartment,
                entrance, phone_number, personal_account, date_task, remark, status_task, purpose,
                registered_residing, address_status, standarts, area, saldo, type_address
            )

    cursor.execute(f""" SELECT * FROM get_meters_data_new({id_user}) """)
    meter_data = cursor.fetchall()

    if meter_data:
        for record in meter_data:
            id_meter, meter_number, instalation_day, meter_type, id_address, meter_remark, marka, seal_number, \
                date_next_verification, location, type_protection = record
            scr.BD.bd_users.local.insert_bd.insert_bd_meters(
                id_meter, meter_number, instalation_day, meter_type, id_address, meter_remark, marka, seal_number,
                date_next_verification, location, type_protection
            )

    cursor.execute(f"""
        SELECT * FROM get_meter_reading_data_new({id_user})
    """)
    meter_reading_data = cursor.fetchall()

    if meter_reading_data:
        for record in meter_reading_data:
            id_meter_reading, meter_id, reading_date, reading_values = record
            scr.BD.bd_users.local.insert_bd.insert_bd_meter_reading(
                id_meter_reading,
                meter_id, reading_date, reading_values
            )

    cursor.close()
    conn.close()


def select_task_data_for_update(id_user):
    res = scr.BD.bd_users.local.select_bd.select_user_data()
    if res:
        for record in res:
            user_id, login, password, privileges, first_name, last_name = record
    conn = scr.func.get_user_db_connection(login, password)
    cursor = conn.cursor()

    cursor.execute(f""" SELECT * FROM get_task_data_new({id_user}) """)
    task_data = cursor.fetchall()

    if task_data:
        for record in task_data:
            task_id, name, address_id, city, district, street, dom, apartment, entrance, \
                registered_residing, address_status, standarts, area, phone_number, \
                personal_account, date_task, remark, status_task, purpose, saldo, type_address = record

            scr.BD.bd_users.local.update_bd.update_tasks_data_from_server(task_id, name, address_id, city, district, street,
                                                                          dom, apartment, entrance,
                                                                          registered_residing, address_status, standarts,
                                                                          area, phone_number,
                                                                          personal_account, date_task, remark, status_task,
                                                                          purpose, saldo)

    cursor.execute(f""" SELECT * FROM get_meters_data_new({id_user}) """)
    meter_data = cursor.fetchall()

    if meter_data:
        for record in meter_data:
            id_meter, meter_number, instalation_day, meter_type, id_address, meter_remark, marka, seal_number, \
                date_next_verification, location = record
            scr.BD.bd_users.local.update_bd.update_meter_data_from_server(id_meter, meter_number, instalation_day, meter_type,
                                                                          id_address, meter_remark, marka, seal_number,
                                                                          date_next_verification, location)
    cursor.execute(f"""
        SELECT * FROM get_meter_reading_data_new({id_user})
    """)
    meter_reading_data = cursor.fetchall()

    if meter_reading_data:
        for record in meter_reading_data:
            id_meter_reading, meter_id, reading_date, reading_values = record
            scr.BD.bd_users.local.update_bd.update_meter_reading_data_from_server(
                id_meter_reading, meter_id, reading_date, reading_values
            )

    cursor.close()
    conn.close()


# переписать отгрузку на сервер новых показаний (пересмотреть запросы)
def upload_data_to_server():
    try:
        res = scr.BD.bd_users.local.select_bd.select_user_data()
        if res:
            for record in res:
                user_id, login, password, privileges, first_name, last_name = record
        conn = scr.func.get_user_db_connection(login, password)
        time_to_server = datetime.datetime.now().strftime("%H:%M:%S")
        result = scr.BD.bd_users.local.select_bd.get_data_to_upload()
        for record in result:
            task_id = record[0]
            unloading_time = record[1]
            last_reading_value = record[2]
            last_reading_date = record[3]
            remark = record[4]
            status = record[5]
            meter_id = record[6]
            meter_remark = record[7]
            cursor = conn.cursor()
            if status == "выполнен":
                cursor.execute(f""" update tasks set uploud_to_local_data = '{unloading_time}',
                 uploud_to_server = '{time_to_server}',remark = '{remark}', status = '{status}' where id = {task_id}""")
                query = f""" insert into meter_reading (meter_id, reading_date, reading_values) values
                            ({meter_id}, '{last_reading_date}', {last_reading_value})"""
                cursor.execute(query)
                query = f""" update  meters set remark = '{meter_remark}' where id = {meter_id} """
                cursor.execute(query)
        conn.commit()
        conn.close()
    except Exception as ex:
        print(ex)
    upload_dop_address_data_to_server()


def upload_dop_address_data_to_server(page):
    try:
        res = scr.BD.bd_users.local.select_bd.select_user_data()
        if res:
            for record in res:
                user_id, login, password, privileges, first_name, last_name = record
        conn = scr.func.get_user_db_connection(login, password)
        cursor = conn.cursor()
        result = scr.BD.bd_users.local.select_bd.get_dop_data_to_upload()
        for record in result:
            addrss_id, registered_residing, address_status, address_standarts, address_area, \
                task_remark, task_id = record
            query = f""" select update_address_task_data (
                {addrss_id}::integer, {registered_residing}::integer, '{address_status}'::varchar, 
                {address_area}::numeric, '{address_standarts}', {task_id}::integer, '{task_remark}'::varchar
            ) """
            cursor.execute(query)
        conn.commit()
        conn.close()
        scr.func.show_snack_bar(page, "Выгруженны все дополнительные данные")
    except Exception as ex:
        scr.func.show_snack_bar(page, "Ошибка выгрузки дополнительных данных")
        print(ex)

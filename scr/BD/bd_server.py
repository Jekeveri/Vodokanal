import os

import psycopg2
import datetime

import scr.BD.bd_users.select_bd
import scr.BD.bd_users.insert_bd
import scr.BD.bd_users.create_bd
import scr.BD.bd_users.update_bd
import scr.func
import scr.navigation_apps.navigations


def check_user_credentials(login, password, page):
    conn = scr.func.get_user_db_connection(login, password)
    if conn is None:
        scr.func.show_snack_bar(page, "Неправильный логин или пароль. Проверьте введенные данные.")
        return
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, e.login, e.password, p.privileges, e.first_name, e.last_name FROM public.employees e
        JOIN public.post p on p.id = e.post_id 
        WHERE login = %s AND password = %s
    """, (login, password))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    scr.BD.bd_users.create_bd.local_user_db()
    if result:
        for record in result:
            id_user, login_user, password_user, privileges, first_name, last_name = record
            if privileges != 1:
                scr.BD.bd_users.insert_bd.insert_bd_user(id_user, login_user, password_user, privileges,
                                                         first_name, last_name, page)
            else:
                scr.navigation_apps.navigations.role_definition(privileges, page)
    else:
        scr.func.show_snack_bar(page, "Нет пользователя в базе данных")  # Нормально написать
        pass


def select_task_data(id_user):
    res = scr.BD.bd_users.select_bd.select_user_data()
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

            scr.BD.bd_users.insert_bd.insert_bd_task(
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
            scr.BD.bd_users.insert_bd.insert_bd_meters(
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
            scr.BD.bd_users.insert_bd.insert_bd_meter_reading(
                id_meter_reading,
                meter_id, reading_date, reading_values
            )

    cursor.close()
    conn.close()


def select_task_data_for_update(id_user):
    res = scr.BD.bd_users.select_bd.select_user_data()
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

            scr.BD.bd_users.update_bd.update_tasks_data_from_server(task_id, name, address_id, city, district, street,
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
            scr.BD.bd_users.update_bd.update_meter_data_from_server(id_meter, meter_number, instalation_day, meter_type,
                                                                    id_address, meter_remark, marka, seal_number,
                                                                    date_next_verification, location)
    cursor.execute(f"""
        SELECT * FROM get_meter_reading_data_new({id_user})
    """)
    meter_reading_data = cursor.fetchall()

    if meter_reading_data:
        for record in meter_reading_data:
            id_meter_reading, meter_id, reading_date, reading_values = record
            scr.BD.bd_users.update_bd.update_meter_reading_data_from_server(
                id_meter_reading, meter_id, reading_date, reading_values
            )

    cursor.close()
    conn.close()


# переписать отгрузку на сервер новых показаний (пересмотреть запсросы)
def upload_data_to_server(page):
    try:
        res = scr.BD.bd_users.select_bd.select_user_data()
        if res:
            for record in res:
                user_id, login, password, privileges, first_name, last_name = record
        conn = scr.func.get_user_db_connection(login, password)
        time_to_server = datetime.datetime.now().strftime("%H:%M:%S")
        result = scr.BD.bd_users.select_bd.get_data_to_upload()
        for record in result:
            task_id = record[0]
            unloading_time = record[1]
            last_reading_value = record[2]
            last_reading_date = record[3]
            remark = record[4]
            status = record[5]
            meter_id = record[6]
            meter_remark = record[7]
            purpose = record[8]
            seal_number = record[9]
            cursor = conn.cursor()
            if status == "выполнен":
                if purpose == "Контрольный съем показаний":
                    cursor.execute(f"""select update_task_meter_data (
                        {task_id}, '{unloading_time}'::time, '{time_to_server}'::time, 
                        '{remark}'::text, '{status}', {meter_id},
                        '{last_reading_date}'::date, {last_reading_value}::numeric, '{meter_remark}'::text
                    )""")
                else:
                    cursor.execute(f"""select update_task_meter_seal (
                        {task_id}::integer, '{unloading_time}'::time, '{time_to_server}'::time,
                        '{remark}'::text, '{status}'::text, {meter_id}::integer, 
                        '{meter_remark}'::text, '{seal_number}'::text
                    )""")
        conn.commit()
        conn.close()
        scr.func.show_snack_bar(page, "Выгруженны данные по выполненым заданиям")
    except Exception as ex:
        print(ex)
        scr.func.show_snack_bar(page, "Произошла ошибка при выгрузке")
    upload_dop_address_data_to_server(page)


def upload_dop_address_data_to_server(page):
    try:
        res = scr.BD.bd_users.select_bd.select_user_data()
        if res:
            for record in res:
                user_id, login, password, privileges, first_name, last_name = record
        conn = scr.func.get_user_db_connection(login, password)
        cursor = conn.cursor()
        result = scr.BD.bd_users.select_bd.get_dop_data_to_upload()
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
        scr.func.show_snack_bar(page,"Выгруженны все дополнительные данные")
    except Exception as ex:
        scr.func.show_snack_bar(page,"Ошибка выгрузки дополнительных данных")
        print(ex)

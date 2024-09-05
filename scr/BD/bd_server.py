import psycopg2
import datetime

import scr.BD.bd_users.select_bd
import scr.BD.bd_users.insert_bd
import scr.BD.bd_users.create_bd
import scr.BD.bd_users.update_bd
import scr.func
import scr.navigation_apps.navigations


def check_user_credentials(login, password, page):
    conn = psycopg2.connect(
        dbname="test",
        user="postgres",
        password='nikita041216'
    )
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
    conn = psycopg2.connect(
        dbname="test",
        user="postgres",
        password='nikita041216'
    )
    cursor = conn.cursor()

    cursor.execute(f""" SELECT * FROM get_task_data_new({id_user}) """)
    task_data = cursor.fetchall()

    if task_data:
        for record in task_data:
            task_id, name, address_id, city, district, street, dom, apartment, entrance, \
                registered_residing, address_status, standarts, area, phone_number, \
                personal_account, date_task, remark, status_task, purpose, saldo = record

            scr.BD.bd_users.insert_bd.insert_bd_task(
                task_id, name, address_id, city, district, street, dom, apartment,
                entrance, phone_number, personal_account, date_task, remark, status_task, purpose,
                registered_residing, address_status, standarts, area, saldo
            )

    cursor.execute(f""" SELECT * FROM get_meters_data_new({id_user}) """)
    meter_data = cursor.fetchall()

    if meter_data:
        for record in meter_data:
            id_meter, meter_number, instalation_day, meter_type, id_address, meter_remark, marka, seal_number, \
                date_next_verification, location = record
            scr.BD.bd_users.insert_bd.insert_bd_meters(
                id_meter, meter_number, instalation_day, meter_type, id_address, meter_remark, marka, seal_number,
                date_next_verification, location
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
    conn = psycopg2.connect(
        dbname="test",
        user="postgres",
        password='nikita041216'
    )
    cursor = conn.cursor()

    cursor.execute(f""" SELECT * FROM get_task_data_new({id_user}) """)
    task_data = cursor.fetchall()

    if task_data:
        for record in task_data:
            task_id, name, address_id, city, district, street, dom, apartment, entrance, \
                registered_residing, address_status, standarts, area, phone_number, \
                personal_account, date_task, remark, status_task, purpose, saldo = record

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
def upload_data_to_server():
    try:
        conn = psycopg2.connect(
            dbname="test",
            user="postgres",
            password=123321
        )
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
            cursor = conn.cursor()
            if status == "выполнен":
                cursor.execute(f""" update tasks set uploud_to_local_data = '{unloading_time}',
                 uploud_to_server = '{time_to_server}',remark = '{remark}', status = '{status}' where id = {task_id}""")
                query = f""" insert into meter_reading (meter_id, reading_date, reading_values) values
                            ({meter_id}, '{last_reading_date}', {last_reading_value})"""
                cursor.execute(query)

        conn.commit()
        conn.close()
    except Exception as ex:
        print(ex)

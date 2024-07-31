import psycopg2

import scr.BD.bd_user
import scr.func
import scr.navigation_apps.navigations


def check_user_credentials(login, password, page):
    conn = psycopg2.connect(
        dbname="test",
        user="postgres",
        password=123321
    )
    cursor = conn.cursor()
    cursor.execute("""
        SELECT e.id, e.login, e.password, p.privileges FROM public.employees e
        JOIN public.post p on p.id = e.post_id 
        WHERE login = %s AND password = %s
    """, (login, password))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    scr.BD.bd_user.local_user_db()
    if result:
        for record in result:
            id_user = record[0]
            login_user = record[1]
            password_user = record[2]
            privileges = record[3]
            if privileges != 1:
                scr.BD.bd_user.insert_bd_user(id_user, login_user, password_user, privileges, page)
            else:
                scr.navigation_apps.navigations.role_definition(privileges, page)
    else:
        scr.func.show_snack_bar(page, "Нет пользователя в базе данных")  # Нормально написать
        pass


def select_task_data(id_user):
    conn = psycopg2.connect(
        dbname="test",
        user="postgres",
        password=123321
    )
    cursor = conn.cursor()
    cursor.execute(f""" SELECT * FROM get_task_data({id_user}) """)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    if result:
        for record in result:
            task_id = record[0]
            name = record[1]
            address = record[2]
            phone_number = record[3]
            email = record[4]
            meter_number = record[5]
            instalation_day = record[6]
            meter_type = record[7]
            last_reading_date = record[8]
            reading_value = record[9]
            date_task = record[10]
            remark = record[11]
            status_task = record[12]
            scr.BD.bd_user.insert_bd_task(task_id, name, address, phone_number, email, meter_number, instalation_day,
                                          meter_type, last_reading_date, reading_value, date_task, remark, status_task)

import psycopg2
import datetime

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
            address_id = record[2]
            city = record[3]
            district = record[4]
            street = record[5]
            dom = record[6]
            apartment = record[7]
            entrance = record[8]
            phone_number = record[9]
            email = record[10]
            meter_number = record[11]
            instalation_day = record[12]
            meter_type = record[13]
            last_reading_date = record[14]
            reading_value = record[15]
            date_task = record[16]
            remark = record[17]
            status_task = record[18]
            meter_id = record[19]
            scr.BD.bd_user.insert_bd_task(task_id, name, address_id, city, district, street, dom, apartment,
                                          entrance, phone_number, email, meter_number, instalation_day,
                                          meter_type, last_reading_date, reading_value, date_task, remark, status_task, meter_id)


def upload_data_to_server():
    try:
        conn = psycopg2.connect(
            dbname="test",
            user="postgres",
            password=123321
        )
        time_to_server = datetime.datetime.now().strftime("%H:%M:%S")
        result = scr.BD.bd_user.get_data_to_upload()
        for record in result:
            task_id = record[0]
            unloading_time = record[1]
            last_reading_value = record[2]
            last_reading_date = record[3]
            remark = record[4]
            status = record[5]
            meter_id = record[6]
            cursor = conn.cursor()
            cursor.execute(f""" update tasks set uploud_to_local_data = '{unloading_time}', 
            uploud_to_server = '{time_to_server}', remark = '{remark}', status = '{status}' where id = {task_id}""")
            # здесь добавить какую-нибудь проверку будет либо инсерт либо апдейт
            query_check = f""" select EXISTS(select * from meter_reading 
            where reading_date = '{last_reading_date}') """
            cursor.execute(query_check)
            result = cursor.fetchall()
            if result==False:
                query = f""" insert into meter_reading (meter_id, reading_date, reading_values) values
                ({meter_id}, '{last_reading_date}',{last_reading_value})"""
                cursor.execute(query)
            else:
                query = f""" update meter_reading set reading_values = {last_reading_value} 
                where meter_id = {meter_id} and reading_date = '{last_reading_date}'"""
                cursor.execute(query)
        conn.commit()
        conn.close()

    except Exception as ex:
        print(ex)

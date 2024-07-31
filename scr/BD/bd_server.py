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
                scr.navigation_apps.navigations.role_definition(privileges,page)
    else:
        scr.func.show_snack_bar(page, "Нет пользователя в базе данных")  # Нормально написать
        pass
import os

import scr.BD.bd_admin.local
import scr.BD.bd_users.local.select_bd
import scr.BD.bd_users.local.insert_bd
import scr.BD.bd_users.local.create_bd
import scr.BD.bd_users.local.update_bd
import scr.func
import scr.navigation_apps.navigations


def check_user_credentials(login, password, page):
    conn = scr.func.get_user_db_connection(login, password)
    if conn is None:
        scr.func.show_snack_bar(page, "Неправильный логин или пароль. Проверьте введенные данные.")
        return
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * from get_employee_by_login_and_password(%, %)
    """, (login, password))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    scr.BD.bd_users.local.create_bd.local_user_db()
    if result:
        for record in result:
            id_user, login_user, password_user, privileges, first_name, last_name = record
            if privileges == 2:
                scr.BD.bd_users.local.insert_bd.insert_bd_user(id_user, login_user, password_user, privileges,
                                                               first_name, last_name, page)
            else:
                scr.BD.bd_admin.local.insert_bd_user(id_user, login_user, password_user, privileges,
                                                     first_name, last_name, page)
    else:
        scr.func.show_snack_bar(page, "Нет пользователя в базе данных")  # Нормально написать
        pass

import os

import scr.BD.bd_server
import scr.BD.bd_users.select_bd
import scr.func
import scr.navigation_apps.navigations
import scr.verifications


def handle_user_sessions(page):
    if os.path.exists("database_client.db"):
        result = scr.BD.bd_users.select_bd.select_user_data()
        if result:  # Проверяем, что содержимое не пустое
            for record in result:
                login = record[0]
                password = record[1]
                privileges = record[2]
                if login != "" and password != "":
                    scr.navigation_apps.navigations.role_definition(privileges, page)
                    scr.func.show_snack_bar(page, "Успешний вход в систему.")
                else:
                    scr.verifications.authentication(page)
        else:
            scr.verifications.authentication(page)
    else:
        scr.verifications.authentication(page)

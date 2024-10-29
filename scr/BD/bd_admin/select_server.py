import scr.func


# Вывод списка назначенных заданий
def select_task_data_all():
    res = scr.BD.bd_users.local.select_bd.select_user_data()
    if res:
        for record in res:
            user_id, login, password, privileges, first_name, last_name = record
    conn = scr.func.get_user_db_connection(login, password)
    cursor = conn.cursor()
    # Тут у нас идет запрос для заполнения таблицы в страничке поиск, нужно будет подкоректировать данные
    try:
        cursor.execute("SELECT * FROM get_task_data_all()")
        results = cursor.fetchall()  # Получаем все записи
        return results
    except Exception as e:
        print(f"Ошибка при выборке данных: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


# Вывод списка сотрудников для его выбора после того, как он выберет задания для назначения
def select_employer_data_statistic_tasks():
    res = scr.BD.bd_users.local.select_bd.select_user_data()
    if res:
        for record in res:
            user_id, login, password, privileges, first_name, last_name = record
    conn = scr.func.get_user_db_connection(login, password)
    cursor = conn.cursor()
    try:
        cursor.execute("Select * from get_list_employer_for_assign_tasks()")
        results = cursor.fetchall()  # Получаем все записи
        return results
    except Exception as e:
        print(f"Ошибка при выборке данных: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


# Вывод списка не назначенных задания для назначения (страница назначения)
def select_task_data_unmade():
    res = scr.BD.bd_users.local.select_bd.select_user_data()
    if res:
        for record in res:
            user_id, login, password, privileges, first_name, last_name = record
    conn = scr.func.get_user_db_connection(login, password)
    cursor = conn.cursor()
    try:
        cursor.execute("Select * from get_task_data_unassigned()")
        results = cursor.fetchall()  # Получаем все записи
        return results
    except Exception as e:
        print(f"Ошибка при выборке данных: {e}")
        return []
    finally:
        cursor.close()
        conn.close()


def select_address_to_choice():
    try:
        res = scr.BD.bd_users.local.select_bd.select_user_data()
        if res:
            for record in res:
                user_id, login, password, privileges, first_name, last_name = record
        conn = scr.func.get_user_db_connection(login, password)
        cursor = conn.cursor()

        cursor.execute(f""" SELECT * FROM show_address_data_to_choice() """)
        data = cursor.fetchall()

        cursor.close()
        conn.close()
        return data
    except Exception as ex:
        print(ex)


def select_employer_to_choice():
    try:
        res = scr.BD.bd_users.local.select_bd.select_user_data()
        if res:
            for record in res:
                user_id, login, password, privileges, first_name, last_name = record
        conn = scr.func.get_user_db_connection(login, password)
        cursor = conn.cursor()

        cursor.execute(f""" SELECT * FROM get_list_employer() """)
        data = cursor.fetchall()

        cursor.close()
        conn.close()
        return data
    except Exception as ex:
        print(ex)

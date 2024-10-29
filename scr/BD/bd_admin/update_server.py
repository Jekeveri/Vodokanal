import os

import psycopg2
import scr.BD.bd_users.select_bd


def set_employer_to_task(task_id, emp_id):
    try:
        res = scr.BD.bd_users.select_bd.select_user_data()
        if res:
            for record in res:
                user_id, login, password, privileges, first_name, last_name = record
        conn = scr.func.get_user_db_connection(login, password)
        cursor = conn.cursor()
        for task_id_ in task_id:
            query = f""" update tasks set emploer_id = {emp_id} where id= {task_id_} """
            cursor.execute(query)

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as ex:
        print(ex)

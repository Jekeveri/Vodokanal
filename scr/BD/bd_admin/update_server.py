import os

import psycopg2

HOST = os.environ.get("HOST", default="localhost")
DBNAME = os.environ.get("DBNAME", default="Vodokanal")
PASSWORD = os.environ.get("PASSWORD", default="1")
USER = os.environ.get("USER", default="postgres")
PORT = os.environ.get("PORT", default="5432")

def set_employer_to_task(task_id, emp_id):
    try:
        conn = psycopg2.connect(
            dbname=DBNAME,
            user=USER,
            password=PASSWORD,
            host=HOST,
            port=PORT
        )
        cursor = conn.cursor()
        for task_id_ in task_id:
            query = f""" update tasks set emploer_id = {emp_id} where id= {task_id_} """
            cursor.execute(query)

        conn.commit()
        cursor.close()
        conn.close()
    except Exception as ex:
        print(ex)

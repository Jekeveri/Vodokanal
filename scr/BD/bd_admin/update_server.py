import psycopg2


def set_employer_to_task(task_id, emp_id):
    try:
        conn = psycopg2.connect(
            dbname="test",
            user="postgres",
            password='123321'
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

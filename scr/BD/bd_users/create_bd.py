import sqlite3 as sl


def local_user_db():
    with sl.connect('database_client.db') as db:
        cursor = db.cursor()
        table_task = """ Create table if not exists tasks(id Integer, name Text, id_address integer, phone_number Text, 
        personal_account Text, date Text, remark Text, status Text, unloading_time Text, purpose Text, saldo Taxt,
        CONSTRAINT task_pk PRIMARY KEY (id)) """
        table_meters = """ Create table if not exists meters(
        id Integer, meter_number Text, instalation_date Text, meter_type text, id_address integer,
        marka Text, seal_number Text, date_next_verification Text, location Text,
        status_filling Text, meter_remark Text, type_protection bool,
        CONSTRAINT meters_pk PRIMARY KEY (id)) """
        table_meter_reading = """ Create table if not exists meter_reading(
        id integer,
        meter_id integer, last_reading_date Text, last_reading_value Text, 
        new_reading_date Text, new_reading_value Text,
        CONSTRAINT meter_reading_pk PRIMARY KEY (id)) """
        table_picture = """ Create table if not exists picture(id Integer primary key autoincrement, value BLOB,
                            name_file Text, task_id Integer, meter_id integer) """
        table_user = """ Create table if not exists user
        (id Integer, login Text, password Text, privileges integer, first_name Text, last_name Text) """
        table_address = """ Create table if not exists address(id integer, city text, district text, street Text, 
        dom text, apartment text, entrance text, registered_residing integer, 
        status Text, standarts REAL, area REAL , type_address Text,
        CONSTRAINT address_pk PRIMARY KEY (id))"""
        cursor.execute(table_task)
        cursor.execute(table_meters)
        cursor.execute(table_meter_reading)
        cursor.execute(table_picture)
        cursor.execute(table_user)
        cursor.execute(table_address)

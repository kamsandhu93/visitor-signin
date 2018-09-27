from visitor_app import app

import sqlite3
import datetime


def login(request_form):
    print(app.config["DB_PATH"])
    first_name = request_form["name"]
    surname = request_form["surname"]
    visiting = request_form["visiting"]

    pass_id = get_unique_pass_code()
    time_in = str(datetime.datetime.now())

    sql = "INSERT INTO visitors (pass_id, first_name, surname, visiting, time_in) " \
          "VALUES (?, ?, ?, ?, ?)"

    execute_modification_sql(sql, [pass_id, first_name, surname, visiting, time_in])

    ''' print pass'''

    return pass_id


def logout(request_form):
    pass_id = request_form["pass_id"]
    time_out = str(datetime.datetime.now())

    sql = "UPDATE visitors " \
          "SET time_out = ? " \
          "WHERE pass_id = ?"

    execute_modification_sql(sql, params=[time_out, pass_id])

    sql = "SELECT first_name, surname " \
          "FROM visitors " \
          "WHERE pass_id = ?"

    full_name = execute_select_sql(sql, params=[pass_id])

    return full_name


def get_unique_pass_code():
    sql = "SELECT last_pass " \
          "FROM settings"

    last_pass_id = execute_select_sql(sql)[0]

    number = int(last_pass_id[:-1])
    if number == 99999:
        number = "00000"
        char = chr(ord(last_pass_id[-1]) + 1)
        pass_code = number + char
    else:
        number += 1
        char = last_pass_id[-1]
        pass_code = str(number).zfill(5) + char

    sql = "UPDATE settings " \
          "SET last_pass = ? " \
          "WHERE pass = 1"

    execute_modification_sql(sql, [pass_code])

    return pass_code


# Prob should put these in a models.py
def execute_modification_sql(sql, params=()):
    conn = sqlite3.connect(app.config["DB_PATH"])
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    conn.close()


def execute_select_sql(sql, params=()):
    conn = sqlite3.connect(app.config["DB_PATH"])
    cursor = conn.cursor()
    cursor.execute(sql, params)
    res = cursor.fetchone()
    conn.close()
    return res


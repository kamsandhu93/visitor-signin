import sqlite3

from dbapi import app


def execute_modification_sql(sql, params=()):
        conn = sqlite3.connect(app.config["DATABASE"])
        cursor = conn.cursor()
        cursor.execute(sql, params)
        app.logger.info("SQL to be committed {}, {}".format(sql, params))
        conn.commit()
        conn.close()
        app.logger.info("Database commit successful")


def execute_select_sql(sql, params=()):
        conn = sqlite3.connect(app.config["DATABASE"])
        cursor = conn.cursor()
        app.logger.info("SQL to be committed {}, {}".format(sql, params))
        cursor.execute(sql, params)
        res = cursor.fetchone()
        conn.close()
        app.logger.info("Database commit successful")
        return res


def log_visitor_in(pass_id, first_name, surname, visiting, company):
    sql = "INSERT INTO visitors (pass_id, first_name, surname, visiting, company, time_in) " \
          "VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)"

    execute_modification_sql(sql, params=[pass_id, first_name, surname, visiting, company])


def log_visitor_out(pass_id):
    sql = "UPDATE visitors " \
          "SET time_out = CURRENT_TIMESTAMP " \
          "WHERE pass_id = ?"

    execute_modification_sql(sql, params=[pass_id])


def get_visitor_full_name(pass_id):
    sql = "SELECT first_name, surname " \
          "FROM visitors " \
          "WHERE pass_id = ?"

    full_name = execute_select_sql(sql, params=[pass_id])

    return full_name


def get_last_pass_id():
    sql = "SELECT last_pass " \
          "FROM settings"

    last_pass_id = execute_select_sql(sql)[0]

    return last_pass_id


def update_last_pass_id(pass_id):
    sql = "UPDATE settings " \
          "SET last_pass = ? " \
          "WHERE pass = 1"

    execute_modification_sql(sql, [pass_id])

def get_logout_time(pass_id):
    sql = "SELECT time_out " \
          "FROM visitors " \
          "WHERE pass_id = ?"

    time_out = execute_select_sql(sql, [pass_id])

    return time_out

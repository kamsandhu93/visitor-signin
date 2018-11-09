import sqlite3

from dbapi import app, exceptions


def executeModificationSql(sql, params=()):
    try:
        conn = sqlite3.connect(app.config["DB_PATH"])
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        conn.close()
    except Exception as ex:
        raise exceptions.DatabaseAccessEx(ex)


def executeSelectSql(sql, params=()):
    try:
        conn = sqlite3.connect(app.config["DB_PATH"])
        cursor = conn.cursor()
        cursor.execute(sql, params)
        res = cursor.fetchone()
        conn.close()
        return res
    except Exception as ex:
        raise exceptions.DatabaseAccessEx(ex)


def logVisitorIn(passId, firstName, surname, visiting, company):
    sql = "INSERT INTO visitors (pass_id, first_name, surname, visiting, company, time_in) " \
          "VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)"

    executeModificationSql(sql, params=[passId, firstName, surname, visiting, company])


def logVisitorOut(passId):
    sql = "UPDATE visitors " \
          "SET time_out = CURRENT_TIMESTAMP " \
          "WHERE pass_id = ?"

    executeModificationSql(sql, params=[passId])


def getVisitorFullName(passId):
    sql = "SELECT first_name, surname " \
          "FROM visitors " \
          "WHERE pass_id = ?"

    full_name = executeSelectSql(sql, params=[passId])

    return full_name


def getLastPassId():
    sql = "SELECT last_pass " \
          "FROM settings"

    lastPassId = executeSelectSql(sql)[0]

    return lastPassId


def updateLastPassId(passId):
    sql = "UPDATE settings " \
          "SET last_pass = ? " \
          "WHERE pass = 1"

    executeModificationSql(sql, [passId])

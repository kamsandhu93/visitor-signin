from flask import Flask, request, render_template
import sqlite3
import datetime


app = Flask(__name__)
DB = "database/visitor_db.db"

@app.route("/")
def view():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    try:
        first_name = request.form["name"]
        surname = request.form["surname"]
        visiting = request.form["visiting"]
        pass_id = get_unique_pass_code()
        time_in = str(datetime.datetime.now())

        sql = "INSERT INTO visitors (pass_id, first_name, surname, visiting, time_in) " \
              "VALUES (?, ?, ?, ?, ?)"

        execute_modification_sql(sql, [pass_id, first_name, surname, visiting, time_in])

        ''' print pass'''

        return render_template("logedin.html", name=first_name, pass_id=pass_id)
    except Exception as ex:
        print(ex)
        return render_template("error.html"), 500


@app.route("/logout", methods=["POST"])
def logout():
    try:
        pass_id = request.form["pass_id"]
        time_out = str(datetime.datetime.now())

        sql = "UPDATE visitors " \
              "SET time_out = ? " \
              "WHERE pass_id = ?"

        execute_modification_sql(sql, params=[time_out, pass_id])

        sql = "SELECT first_name, surname " \
              "FROM visitors " \
              "WHERE pass_id = ?"

        full_name = execute_select_sql(sql, params=[pass_id])

        return render_template("logedout.html", first_name=full_name[0], surname=full_name[1])
    except Exception as ex:
        print(ex)
        return render_template("error.html"), 500


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

def execute_modification_sql(sql, params=()):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    conn.close()


def execute_select_sql(sql, params=()):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute(sql, params)
    res = cursor.fetchone()
    conn.close()
    return res


if __name__ == "__main__":
    app.run(host='0.0.0.0')

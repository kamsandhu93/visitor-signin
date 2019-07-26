import datetime
import json
import os
import sqlite3
import unittest

from dbapi import app
from sqlite3 import Error


TEMP_DB = 'temp_test_db.db'
CREATE_VISITORS_SQL = """CREATE TABLE 'visitors' (
    'pass_id' TEXT UNIQUE,
    'first_name' TEXT NOT NULL,
    'surname' TEXT NOT NULL,
    'visiting' TEXT NOT NULL,
    'time_in' TEXT,
    'time_out' TEXT,
    'company' TEXT
)"""
CREATE_SETTINGS_SQL = """CREATE TABLE 'settings' (
    'pass' INTEGER,
    'last_pass' TEXT
)
"""
ADD_PASS_SQL = """ INSERT INTO settings VALUES (1, '00000a')"""


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEMP_DB):
            os.remove(TEMP_DB)

        self.create_db(TEMP_DB)
        self.temp_database_path = os.path.abspath(TEMP_DB)
        self.app = app
        self.app.config['DATABASE'] = self.temp_database_path
        self.app_test_client = self.app.test_client()

    def tearDown(self):
        os.remove(self.temp_database_path)

    @staticmethod
    def create_db(db_file):
        """ create a database connection to a SQLite database """
        try:
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute(CREATE_VISITORS_SQL)
            cursor.execute(CREATE_SETTINGS_SQL)
            cursor.execute(ADD_PASS_SQL)
            conn.commit()
            conn.close()
            app.logger.info("Database commit successful")
        except Error as e:
            print(e)
            raise

    def get_all_data_from_db_table(self, table):
        conn = sqlite3.connect(self.temp_database_path)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM {}'.format(table))
        res = cursor.fetchall()
        conn.close()
        return res


class HappyPathTestCase(BaseTestCase):

    def test_login_then_logout(self):
        ##### TEST 1 login and logout with out company #####

        #login
        login_request = {
            "name": "mak",
            "surname": "uhdnas",
            "visiting": "anker"
        }
        with self.app_test_client as client:
            result = client.post('/login',
                                 data=json.dumps(login_request),
                                 content_type='application/json')
            self.assertEqual('200 OK', result.status)
            self.assertEqual(json.dumps({'passId': '00001a'}), json.dumps(result.json))

            db_data = self.get_all_data_from_db_table('visitors')
            self.assertTrue(db_data[0], 'No row in db')
            row = db_data[0]
            self.assertEqual(row[0], result.json['passId'])
            self.assertEqual(row[1], login_request['name'])
            self.assertEqual(row[2], login_request['surname'])
            self.assertEqual(row[3], login_request['visiting'])
            self.assertTrue(datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S'))  # checking is date
            self.assertIsNone(row[5], 'Unexpected log out time on db')
            self.assertIsNone(row[6], 'Unexpected company on db')

        # logout
        logout_request = {
            "passId": result.json['passId'],
        }
        with self.app_test_client as client:
            result_2 = client.post('/logout',
                                 data=json.dumps(logout_request),
                                 content_type='application/json')
            self.assertEqual('200 OK', result_2.status)
            self.assertEqual(json.dumps({'firstName': login_request['name'], 'surname': login_request['surname']}), json.dumps(result_2.json))

            db_data = self.get_all_data_from_db_table('visitors')
            row = db_data[0]
            self.assertIsNotNone(row[5], 'Log out time not recorded on database')
            self.assertTrue(datetime.datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S'))  # checking is valid date

        ##### TEST 2 login and logout with company #####
        # login
        login_request = {
            "name": "darb",
            "surname": "gnaw",
            "visiting": "rekna",
            "company": "digitalnhs"
        }

        with self.app_test_client as client:
            result = client.post('/login',
                                 data=json.dumps(login_request),
                                 content_type='application/json')
            self.assertEqual('200 OK', result.status)
            self.assertEqual(json.dumps({'passId': '00002a'}), json.dumps(result.json))

            db_data = self.get_all_data_from_db_table('visitors')
            self.assertTrue(db_data[1], 'No row in db')
            row = db_data[1]
            self.assertEqual(row[0], result.json['passId'])
            self.assertEqual(row[1], login_request['name'])
            self.assertEqual(row[2], login_request['surname'])
            self.assertEqual(row[3], login_request['visiting'])
            self.assertTrue(datetime.datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')) # just checking is date
            self.assertIsNone(row[5])
            self.assertEqual(row[6], login_request['company'])


        # logout
        logout_request = {
            "passId": result.json['passId'],
        }
        with self.app_test_client as client:
            result_2 = client.post('/logout',
                                 data=json.dumps(logout_request),
                                 content_type='application/json')
            self.assertEqual('200 OK', result_2.status)
            self.assertEqual(json.dumps({'firstName': login_request['name'], 'surname': login_request['surname']}),
                             json.dumps(result_2.json))

            db_data = self.get_all_data_from_db_table('visitors')
            row = db_data[0]
            self.assertIsNotNone(row[5], 'Log out time not recorded on database')
            self.assertTrue(datetime.datetime.strptime(row[5], '%Y-%m-%d %H:%M:%S'))# checking is valid date


if __name__ == '__main__':
    unittest.main()

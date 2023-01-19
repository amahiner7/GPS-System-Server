import pymysql
from urllib.parse import urlsplit, parse_qsl
from datetime import datetime


class DatabaseService:
    def __init__(self):
        self.db_ip = ""
        self.db_port = 0
        self.db_name = ""
        self.db_id = ""
        self.db_password = ""
        self.db_conn = None
        self.db_cursor = None
        self.connected = False

    def __check_db_conn(self):
        if self.db_conn is None or self.db_cursor is None:
            self.re_connect()

    def __close_db(self):
        try:
            if self.db_cursor is not None:
                self.db_cursor.close()

            if self.db_conn is not None:
                self.db_conn.close()
        except Exception as ex:
            print("DatabaseService.__close_db():", ex)
        finally:
            self.db_cursor = None
            self.db_conn = None

    def connect(self, db_ip, db_port, id, password, db_name, print_msg=True):
        self.db_ip = db_ip
        self.db_port = db_port
        self.db_id = id
        self.db_password = password
        self.db_name = db_name

        try:
            self.db_conn = pymysql.connect(
                user=id,
                password=password,
                host=db_ip,
                port=db_port,
                db=db_name,
                charset='utf8'
            )

            self.db_cursor = self.db_conn.cursor(pymysql.cursors.DictCursor)
            if print_msg:
                print(f"Connect to {self.db_ip}, {db_name} success.")
            self.connected = True
            return True

        except Exception as ex:
            if print_msg:
                print(f"Connect to {db_ip}, {db_name} is failed.")
            print(str(ex))
            self.connected = False
            return False

    def re_connect(self):
        result = self.connect(
            db_ip=self.db_ip,
            db_port=self.db_port,
            id=self.db_id,
            password=self.db_password,
            db_name=self.db_name,
            print_msg=False)

        return result

    def is_connected(self):
        return self.connected

    def get_par_data(self, co_div):
        sql = "SELECT COUR_NAME, COUR_NAME_S, " \
              "HOLE_NO_01, HOLE_NO_02, HOLE_NO_03, HOLE_NO_04, HOLE_NO_05, " \
              "HOLE_NO_06, HOLE_NO_07, HOLE_NO_08, HOLE_NO_09, " \
              "PAR_CNT_01, PAR_CNT_02, PAR_CNT_03, PAR_CNT_04, PAR_CNT_05, " \
              "PAR_CNT_06, PAR_CNT_07, PAR_CNT_08, PAR_CNT_09 " \
              "FROM GA0200 " \
              f"WHERE CO_DIV = {co_div} " \
              "ORDER BY COUR_CD; "
        try:
            self.db_cursor.execute(sql)
        except Exception as ex:
            print("DatabaseService.get_par_data():", ex)
            return {'resultCode': 500, 'resultMsg': 'query execution fail.'}

        results = [dict((self.db_cursor.description[i][0], value) for i, value in enumerate(row.values()))
                   for row in self.db_cursor.fetchall()]

        if results is not None and len(results) > 0:
            return results
        else:
            return None

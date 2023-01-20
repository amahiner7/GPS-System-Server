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
              f"WHERE CO_DIV = '{co_div}' " \
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

    def get_hole_par_data(self, co_div, cour_name):
        sql = "SELECT " \
              "HOLE_NO_01, HOLE_NO_02, HOLE_NO_03, HOLE_NO_04, HOLE_NO_05, " \
              "HOLE_NO_06, HOLE_NO_07, HOLE_NO_08, HOLE_NO_09, " \
              "PAR_CNT_01, PAR_CNT_02, PAR_CNT_03, PAR_CNT_04, PAR_CNT_05, " \
              "PAR_CNT_06, PAR_CNT_07, PAR_CNT_08, PAR_CNT_09 " \
              "FROM GA0200 " \
              "WHERE 1 = 1 " \
              f"AND CO_DIV = '{co_div}' "\
              f"AND COUR_NAME = '{cour_name}' " \
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

    def get_gps_score_data(self, co_div, game_sid):
        sql = "SELECT G.COUR_CD_P, G.GAME_SID, G.CHANGE_CD_P, G.CHANGE_CD_N, G.CHANGE_CD_A, P.CHKIN_NO, P.CUST_NM, " \
              "CASE WHEN S.COURSE_A IS NULL THEN G.CHANGE_CD_P ELSE S.COURSE_A END COURSE_A, " \
              "CASE WHEN S.SCORE_A1 IS NULL THEN 0 ELSE S.SCORE_A1 END SCORE_A1, " \
              "CASE WHEN S.SCORE_A2 IS NULL THEN 0 ELSE S.SCORE_A2 END SCORE_A2, " \
              "CASE WHEN S.SCORE_A3 IS NULL THEN 0 ELSE S.SCORE_A3 END SCORE_A3, " \
              "CASE WHEN S.SCORE_A4 IS NULL THEN 0 ELSE S.SCORE_A4 END SCORE_A4, " \
              "CASE WHEN S.SCORE_A5 IS NULL THEN 0 ELSE S.SCORE_A5 END SCORE_A5, " \
              "CASE WHEN S.SCORE_A6 IS NULL THEN 0 ELSE S.SCORE_A6 END SCORE_A6, " \
              "CASE WHEN S.SCORE_A7 IS NULL THEN 0 ELSE S.SCORE_A7 END SCORE_A7, " \
              "CASE WHEN S.SCORE_A8 IS NULL THEN 0 ELSE S.SCORE_A8 END SCORE_A8, " \
              "CASE WHEN S.SCORE_A9 IS NULL THEN 0 ELSE S.SCORE_A9 END SCORE_A9, " \
              "CASE WHEN S.COURSE_B IS NULL THEN G.CHANGE_CD_N ELSE S.COURSE_B END COURSE_B, " \
              "CASE WHEN S.SCORE_B1 IS NULL THEN 0 ELSE S.SCORE_B1 END SCORE_B1, " \
              "CASE WHEN S.SCORE_B2 IS NULL THEN 0 ELSE S.SCORE_B2 END SCORE_B2, " \
              "CASE WHEN S.SCORE_B3 IS NULL THEN 0 ELSE S.SCORE_B3 END SCORE_B3, " \
              "CASE WHEN S.SCORE_B4 IS NULL THEN 0 ELSE S.SCORE_B4 END SCORE_B4, " \
              "CASE WHEN S.SCORE_B5 IS NULL THEN 0 ELSE S.SCORE_B5 END SCORE_B5, " \
              "CASE WHEN S.SCORE_B6 IS NULL THEN 0 ELSE S.SCORE_B6 END SCORE_B6, " \
              "CASE WHEN S.SCORE_B7 IS NULL THEN 0 ELSE S.SCORE_B7 END SCORE_B7, " \
              "CASE WHEN S.SCORE_B8 IS NULL THEN 0 ELSE S.SCORE_B8 END SCORE_B8, " \
              "CASE WHEN S.SCORE_B9 IS NULL THEN 0 ELSE S.SCORE_B9 END SCORE_B9, " \
              "CASE WHEN S.SCORE_TOTAL_A IS NULL THEN 0 ELSE S.SCORE_TOTAL_A END SCORE_TOTAL_A, " \
              "CASE WHEN S.SCORE_TOTAL_B IS NULL THEN 0 ELSE S.SCORE_TOTAL_B END SCORE_TOTAL_B, " \
              "CASE WHEN S.SCORE_TOTAL   IS NULL THEN 0 ELSE S.SCORE_TOTAL   END SCORE_TOTAL, " \
              "G.SCORE_PIC_URL1, S.SMS_SEND , H.EN_PHONE " \
              "FROM  GC0110 P INNER JOIN GD0100 G ON G.CO_DIV = P.CO_DIV " \
              "AND G.GAME_DT = P.GAME_DT " \
              "AND G.GAME_SID = P.GAME_SID " \
              "INNER JOIN GD0300 S ON P.CO_DIV = S.CO_DIV " \
              "AND P.GAME_DT = S.GAME_DT " \
              "AND P.CHKIN_NO = S.CHKIN_NO " \
              "AND S.GAME_SID = P.GAME_SID " \
              "INNER JOIN EN_HISTORY H ON G.CO_DIV = H.CO_DIV " \
              "AND G.GAME_DT = H.EN_DAY " \
              "AND G.COUR_CD_P = H.EN_COS AND G.GAME_TI = H.EN_TIME and P.CHKIN_NO = H.en_chkinno " \
              f"WHERE P.CO_DIV = '{co_div}' " \
              "AND P.CHECKINYN = 'Y' " \
              f"AND p.game_sid ='{game_sid}' " \
              "AND G.DEL_YN = 'N' " \
              "ORDER by S.EN_SEQ ASC; "
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

    def get_total_gps_score_information(self):

        pass

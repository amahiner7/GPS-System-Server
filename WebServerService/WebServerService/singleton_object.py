import os
import sys
from enum import Enum

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from Config.configs import Configs
from DataService.database_service import DatabaseService
from WebServerService.settings import LOG_INSERT_DATABASE
# from settings import LOG_INSERT_DATABASE


class LotType(Enum):
    Info = 0
    Warn = 1
    Error = 2


class SingletonObject:
    database_service = DatabaseService()
    gps_database_service = DatabaseService()


class LogService:
    @staticmethod
    def Info(log_text, date_time=None):
        print(log_text)
        if LOG_INSERT_DATABASE:
            SingletonObject.gps_database_service.insert_server_log(
                log_text=log_text, log_type=LotType.Info.name, date_time=date_time)

    @staticmethod
    def Warn(log_text, date_time=None):
        print(log_text)
        if LOG_INSERT_DATABASE:
            SingletonObject.gps_database_service.insert_server_log(
                log_text=log_text, log_type=LotType.Warn.name, date_time=date_time)

    @staticmethod
    def Error(log_text, date_time=None):
        print(log_text)
        if LOG_INSERT_DATABASE:
            SingletonObject.gps_database_service.insert_server_log(
                log_text=log_text, log_type=LotType.Error.name, date_time=date_time)


def connect_to_database_server():
    if not SingletonObject.database_service.is_connected():
        SingletonObject.database_service.connect(
            db_ip=Configs.clubd_default_db_ip,
            db_port=Configs.clubd_default_db_port,
            id=Configs.clubd_default_db_id,
            password=Configs.clubd_default_db_password,
            db_name=Configs.clubd_default_db_name)

    if not SingletonObject.gps_database_service.is_connected():
        SingletonObject.gps_database_service.connect(
            db_ip=Configs.gps_default_db_ip,
            db_port=Configs.gps_default_db_port,
            id=Configs.gps_default_db_id,
            password=Configs.gps_default_db_password,
            db_name=Configs.gps_default_db_name)


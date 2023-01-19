from Config.configs import Configs
from DataService.database_service import DatabaseService


class SingletonObject:
    database_service = DatabaseService()


def connect_to_database_server():
    if not SingletonObject.database_service.is_connected():
        SingletonObject.database_service.connect(
            db_ip=Configs.clubd_default_db_ip,
            db_port=Configs.clubd_default_db_port,
            id=Configs.clubd_default_db_id,
            password=Configs.clubd_default_db_password,
            db_name=Configs.clubd_default_db_name)
import argparse


def load_command_args():
    parser = argparse.ArgumentParser(description="GPS System Server")
    parser.add_argument("--db_ip", type=str, default=Configs.default_db_ip)
    parser.add_argument("--db_port", type=str, default=Configs.default_db_port)
    parser.add_argument("--db_name", type=str, default=Configs.default_db_name)
    parser.add_argument("--db_id", type=str, default=Configs.default_db_id)
    parser.add_argument("--db_password", type=str, default=Configs.default_db_password)
    Configs.args = parser.parse_args()

    Configs.db_ip = Configs.args.db_ip
    Configs.db_name = Configs.args.db_name
    Configs.db_id = Configs.args.db_id
    Configs.db_password = Configs.args.db_password


class Configs:
    gps_default_db_ip = "127.0.0.1"
    gps_default_db_port = 3307
    gps_default_db_name = "gps_system_server"
    gps_default_db_id = "greenitgps"
    gps_default_db_password = "j#u19OI@n0%)f@5"

    clubd_default_db_ip = "202.68.227.57"
    clubd_default_db_port = 13306
    clubd_default_db_name = "bear"
    clubd_default_db_id = "greenit"
    clubd_default_db_password = "greenitgps^@@*6228"

    db_ip = ""
    db_name = ""
    db_id = ""
    db_password = ""

    args = None

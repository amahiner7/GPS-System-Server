import os
from django.utils import timezone


class Configs:
    upload_file_path = ""


def set_upload_file_path(upload_file_path):
    Configs.upload_file_path = upload_file_path


def get_upload_file_path(instance, filename):
    date_time = timezone.now().strftime("%Y%m%d")
    result_path = f"{Configs.upload_file_path}/{date_time}"

    if not os.path.exists(result_path):
        os.makedirs(result_path)

    result_path = f"{result_path}/{filename}"

    return result_path
222
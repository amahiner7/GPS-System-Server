import os
from django.utils import timezone


class Configs:
    sub_upload_file_path = ""


def set_sub_upload_file_path(sub_upload_file_path):
    Configs.sub_upload_file_path = sub_upload_file_path


def get_upload_file_path(instance, filename, media_root, sub_upload_file_path=None):
    date_time = timezone.now().strftime("%Y%m%d")

    if sub_upload_file_path is None:
        sub_upload_file_path = Configs.sub_upload_file_path

    result_path = f"{media_root}/{sub_upload_file_path}/{date_time}"

    if not os.path.exists(result_path):
        os.makedirs(result_path)

    result_path = f"{result_path}/{filename}"

    return result_path

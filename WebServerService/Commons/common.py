import os
import requests
from django.utils import timezone
from WebServerService.settings import MEDIA_ROOT
import WebServerService.settings


def set_upload_file_path(upload_file_path):
    WebServerService.settings.UPLOAD_FILE_PATH = upload_file_path


def get_upload_file_path(instance, filename):
    date_time = timezone.now().strftime("%Y%m%d")
    result_path = f"{WebServerService.settings.UPLOAD_FILE_PATH}/{date_time}"

    if not os.path.exists(result_path):
        os.makedirs(result_path)

    result_path = f"{result_path}/{filename}"

    return result_path


def get_public_ip_address():
    ip_address = requests.get("https://api.ipify.org").text
    return ip_address

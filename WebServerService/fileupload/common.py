import os
from django.utils import timezone


def get_upload_file_path(instance, filename, gc_no, fname):
    date_time = timezone.now().strftime("%Y%m%d")
    result_path = os.path.join(instance.name, gc_no)
    result_path = os.path.join(result_path, fname)
    result_path = os.path.join(result_path, date_time)
    result_path = os.path.join(result_path, filename)

    return result_path

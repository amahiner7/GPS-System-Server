import os
import sys
from django.db import models

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from Commons.common import get_upload_file_path


class FileInformation(models.Model):
    title = models.CharField(max_length=256, null=True)
    gc_no = models.CharField(max_length=256, null=True)
    fname = models.CharField(max_length=256, null=True)
    toUpFile = models.FileField(upload_to=get_upload_file_path, blank=True)
    toUpFile_url = models.CharField(max_length=256, null=True)
    datetime = models.DateTimeField(auto_now_add=True)

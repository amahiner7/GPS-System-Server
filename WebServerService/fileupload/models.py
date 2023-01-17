from django.db import models
from functools import partial
from .common import get_upload_file_path


class FileInformation(models.Model):
    title = models.CharField(max_length=256, null=True)
    gc_no = models.CharField(max_length=256, null=True)
    fname = models.CharField(max_length=256, null=True)
    toUpFile = models.FileField(upload_to=partial(get_upload_file_path, gc_no=gc_no, fname=fname), blank=True)
    toUpFile_url = models.CharField(max_length=256, null=True)
    datetime = models.DateTimeField(auto_now_add=True)

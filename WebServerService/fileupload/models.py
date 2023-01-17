from django.db import models


class FileInformation(models.Model):
    title = models.CharField(max_length=256, null=True)
    gc_no = models.CharField(max_length=256, null=True)
    fname = models.CharField(max_length=256, null=True)
    toUpFile = models.FileField(upload_to="", blank=True)
    toUpFile_url = models.CharField(max_length=256, null=True)
    datetime = models.DateTimeField(auto_now_add=True)

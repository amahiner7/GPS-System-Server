from django.db import models


class FileUpload(models.Model):
    title = models.CharField(max_length=256, null=True)
    imgfile = models.ImageField(upload_to="", blank=True)
    datetime = models.DateTimeField(auto_now_add=True)

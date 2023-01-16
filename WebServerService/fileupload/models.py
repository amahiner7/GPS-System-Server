from django.db import models


class FileInformation(models.Model):
    title = models.CharField(max_length=256, null=True)
    image = models.ImageField(upload_to="", blank=True)
    image_url = models.CharField(max_length=256, null=True)
    datetime = models.DateTimeField(auto_now_add=True)

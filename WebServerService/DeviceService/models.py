from django.db import models

# Create your models here.
from django.db import models


class DeviceLog(models.Model):
    log = models.TextField()
    type = models.CharField(max_length=255)
    datetime = models.DateTimeField("log date time")

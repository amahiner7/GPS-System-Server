from django.db import models

# Create your models here.
from django.db import models


class DeviceLog(models.Model):
    log = models.TextField()
    type = models.CharField(max_length=255)
    datetime = models.DateTimeField(auto_now_add=True)


class FileUpload(models.Model):
    title = models.CharField(max_length=256, null=True)
    imgfile = models.ImageField(upload_to="", blank=True)
    datetime = models.DateTimeField(auto_now_add=True)


# class Product(models.Model):
#     modify_date = models.DateTimeField(null=True, blank=True)
#     pcode = models.CharField(max_length=10)
#     pname = models.TextField()
#     unitprice = models.IntegerField(default=0)
#     discountrate = models.DecimalField(max_digits=11, decimal_places=2,default=0)
#     mainfunc = models.CharField(max_length=100, default="")
#     imgfile = models.ImageField(null=True, upload_to="", blank=True) # 이미지 컬럼 추가
#     detailfunc = models.CharField(max_length=200, default="")

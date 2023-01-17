from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.fileupload, name="fileupload"),
    # path("fileupload_test", views.fileupload, name="fileupload"),
    path("filelist", views.filelist, name="filelist"),
    path("filelist/", views.filelist, name="filelist")
]

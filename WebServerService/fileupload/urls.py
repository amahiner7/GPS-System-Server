from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.fileupload, name="fileupload"),
    # path("fileupload/", views.fileupload, name="fileupload"),
    path("filelist/", views.filelist, name="filelist")
]

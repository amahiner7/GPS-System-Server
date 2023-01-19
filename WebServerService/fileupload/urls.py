from django.urls import path
from . import views
from .fileupload_view import FileUploadView

# app_name = "fileupload"

urlpatterns = [
    path("", views.filelist, name="filelist"),
    path("list", views.filelist, name="filelist"),
    path("list/", views.filelist, name="filelist"),
    path("upload", FileUploadView.as_view(), name="fileupload"),
    path("upload/", FileUploadView.as_view(), name="fileupload"),
    path("download/<str:gc_no>", views.filedownload, name="filedownload"),
]

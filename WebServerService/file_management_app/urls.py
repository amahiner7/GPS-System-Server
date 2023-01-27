from django.urls import path
from . import views
from .file_upload_view import FileUploadView
from .file_list_view import FileListView
from .file_download_view import FileDownloadView

# app_name = "fileupload"

urlpatterns = [
    path("/<str:param>", FileDownloadView.as_view(), name="filedownload"),
    path("download/<str:param>", FileDownloadView.as_view(), name="filedownload"),
    path("list", FileListView.as_view(), name="filelist"),
    path("list/", FileListView.as_view(), name="filelist"),
    path("upload", FileUploadView.as_view(), name="fileupload"),
    path("upload/", FileUploadView.as_view(), name="fileupload"),
]
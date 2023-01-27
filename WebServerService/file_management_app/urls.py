from django.urls import path
from .file_upload_view import FileUploadView
from .file_list_view import FileListView
from .file_download_view import FileDownloadView

urlpatterns = [
    path("/<str:param>", FileDownloadView.as_view(), name="download"),
    path("download/<str:param>", FileDownloadView.as_view(), name="download"),
    path("list", FileListView.as_view(), name="list"),
    path("list/", FileListView.as_view(), name="list"),
    path("upload", FileUploadView.as_view(), name="fileupload"),
    path("upload/", FileUploadView.as_view(), name="fileupload"),
]

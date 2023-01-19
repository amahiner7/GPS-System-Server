from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # path("list", views.filelist, name="filelist"),
    # path("list/", views.filelist, name="filelist"),
    # path("upload", views.fileupload, name="fileupload"),
    # path("upload/", views.fileupload, name="fileupload"),
    # path("download/<str:gc_no>", views.filedownload, name="filedownload"),
]

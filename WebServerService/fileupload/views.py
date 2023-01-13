import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import FileUploadForm
from .models import FileInformation
import socket


def fileupload(request):
    if request.method == "GET":
        fileuploadForm = FileUploadForm
        context = \
            {
                'fileuploadForm': fileuploadForm,
            }
        return render(request, 'fileupload/fileupload.html', context)

    elif request.method == 'POST':
        image_file = request.FILES["image_file"]
        title = os.path.basename(image_file.name)

        file_information = FileInformation(
            title=title,
            image_file=image_file,
        )
        file_information.save()

        image_file_url = f"http://{socket.gethostbyname(socket.gethostname())}:8080/imagefile/{image_file.name}"
        result = {"rCode": "0", "rMessage": "Success", "file_url": image_file_url}
        return JsonResponse(result, safe=False)

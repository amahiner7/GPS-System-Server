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
        image = request.FILES["image"]
        title = os.path.basename(image.name)
        image_url = f"http://{socket.gethostbyname(socket.gethostname())}:8080/image/{image.name}"

        file_information = FileInformation(
            title=title,
            image=image,
            image_url=image_url
        )
        file_information.save()

        result = {"rCode": "0", "rMessage": "Success", "file_url": image_url}
        return JsonResponse(result, safe=False)


def filelist(request):
    file_information = FileInformation.objects.all()

    return render(
        request, 'fileupload/filelist.html',
        {
            'file_information': file_information
        }
    )

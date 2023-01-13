from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import FileUploadForm
from .models import FileUpload


def fileupload(request):
    if request.method == "GET":
        fileuploadForm = FileUploadForm
        context = \
        {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'DeviceService/fileupload.html', context)

    elif request.method == 'POST':
        title = request.POST['title']
        imgfile = request.FILES["imgfile"]
        fileupload = FileUpload(
            title=title,
            imgfile=imgfile,
        )
        fileupload.save()

        result = {"rCode": "0", "rMessage": "Success"}
        return JsonResponse(result, safe=False)

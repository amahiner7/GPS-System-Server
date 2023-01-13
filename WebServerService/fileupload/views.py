from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import FileUploadForm
from .models import FileInformation


def fileupload(request):
    if request.method == "GET":
        fileuploadForm = FileUploadForm
        context = \
            {
                'fileuploadForm': fileuploadForm,
            }
        return render(request, 'fileupload/fileupload.html', context)

    elif request.method == 'POST':
        title = request.POST['title']
        image_file = request.FILES["image_file"]
        file_information = FileInformation(
            title=title,
            image_file=image_file,
        )
        file_information.save()

        result = {"rCode": "0", "rMessage": "Success"}
        return JsonResponse(result, safe=False)

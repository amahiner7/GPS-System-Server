import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
import socket
from .forms import FileUploadForm
from .models import FileInformation
from .models import get_upload_file_path


@csrf_exempt
def fileupload(request):
    if request.method == "GET":
        try:
            fileuploadForm = FileUploadForm
            context = \
                {
                    'fileuploadForm': fileuploadForm,
                }
            return render(request, 'fileupload/fileupload.html', context)
        except Exception as ex:
            result = {'rCode': 500, 'rMessage': str(ex)}
            return JsonResponse(result, safe=False)

    elif request.method == 'POST':
        try:
            gc_no = request.POST["gc_no"]
            fname = request.POST["fname"]
            toUpFile = request.FILES["toUpFile"]
            title = os.path.basename(toUpFile.name)

            # upload_file_path = get_upload_file_path()
            # if not os.path.exists(upload_file_path):
            #     os.makedirs(upload_file_path)

            toUpFile_url = f"http://{socket.gethostbyname(socket.gethostname())}:8080/image/{toUpFile.name}"

            file_information = FileInformation(
                title=title,
                gc_no=gc_no,
                fname=fname,
                toUpFile=toUpFile,
                toUpFile_url=toUpFile_url
            )

            file_information.save()

            result = {"rCode": "0", "rMessage": "Success", "file_url": toUpFile_url}
            return JsonResponse(result, safe=False)
        except Exception as ex:
            result = {'rCode': 500, 'rMessage': str(ex)}
            return JsonResponse(result, safe=False)


@csrf_exempt
def filelist(request):
    file_information = FileInformation.objects.all()

    return render(
        request, 'fileupload/filelist.html',
        {
            'file_information': file_information
        }
    )

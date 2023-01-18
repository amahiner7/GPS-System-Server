import os
import sys
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
import socket
from .forms import FileUploadForm
from .models import FileInformation
from .common import *

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from WebServerService.settings import MEDIA_ROOT


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

            upload_file_path = f"{MEDIA_ROOT}/{gc_no}/{fname}"
            set_upload_file_path(upload_file_path=upload_file_path)

            date_time = timezone.now().strftime("%Y%m%d")
            sub_upload_web_url = f"{gc_no}/{fname}/{date_time}"

            toUpFile_url = \
                f"http://{socket.gethostbyname(socket.gethostname())}:8080/image/{sub_upload_web_url}/{toUpFile.name}"

            file_information = FileInformation(
                title=title,
                gc_no=gc_no,
                fname=fname,
                toUpFile=toUpFile,
                toUpFile_url=toUpFile_url
            )

            file_information.save()

            result = {"rCode": "200", "rMessage": "Success", "file_url": toUpFile_url}
            return JsonResponse(result, safe=False)
        except Exception as ex:
            result = {'rCode': 500, 'rMessage': str(ex)}
            return JsonResponse(result, safe=False)


@csrf_exempt
def filelist(request):
    if request.method == "GET":
        file_information = FileInformation.objects.all()

        return render(
            request, 'fileupload/filelist.html',
            {
                'file_information': file_information
            }
        )


@csrf_exempt
def filedownload(request, gc_no):
    if request.method == "GET":
        try:
            fname = request.GET['fname']
            datetime = request.GET['datetime']
            filename = request.GET['filename']

            file_path = f"{MEDIA_ROOT}/{gc_no}/{fname}/{datetime}/{filename}"

            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="image/png")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
            else:
                result = {'rCode': 400, 'rMessage': "Bad request"}
                return JsonResponse(result, safe=False)

        except Exception as ex:
            result = {'rCode': 500, 'rMessage': str(ex)}
            return JsonResponse(result, safe=False)

import os
import sys
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import socket
from .forms import FileUploadForm
from .models import FileInformation

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from Commons.common import *
from WebServerService.settings import MEDIA_ROOT, SERVER_NAT_IP_ADDRESS


@method_decorator(csrf_exempt, name="dispatch")
class FileUploadView(View):
    def get(self, request):
        try:
            fileuploadForm = FileUploadForm
            context = \
                {
                    'fileuploadForm': fileuploadForm,
                }
            return render(request, 'file_management_app/fileupload.html', context)
        except Exception as ex:
            result = {'rCode': 500, 'rMessage': str(ex)}
            return JsonResponse(result, safe=False)

    def post(self, request):
        try:
            gc_no = request.POST["gc_no"]
            fname = request.POST["fname"]
            toUpFile = request.FILES["toUpFile"]
            title = os.path.basename(toUpFile.name)

            upload_file_path = f"{MEDIA_ROOT}/{gc_no}/{fname}"
            set_upload_file_path(upload_file_path=upload_file_path)

            date_time = timezone.now().strftime("%Y%m%d")

            sub_upload_web_url = f"{gc_no}/{fname}/{date_time}"

            # ip_address = get_public_ip_address()
            ip_address = SERVER_NAT_IP_ADDRESS

            toUpFile_url = \
                f"http://{ip_address}:8080/image/{sub_upload_web_url}/{toUpFile.name}"

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

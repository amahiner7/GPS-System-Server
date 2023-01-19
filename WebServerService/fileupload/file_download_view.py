import os
import sys
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from Commons.common import *
from WebServerService.settings import MEDIA_ROOT


@method_decorator(csrf_exempt, name="dispatch")
class FileDownloadView(View):
    def get(self, request, gc_no):
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

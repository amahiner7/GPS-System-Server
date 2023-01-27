import os
import sys
from django.views import View
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from Commons.common import *
from WebServerService.settings import MEDIA_ROOT, GPS_SCORE_APP_STATIC_ROOT


@method_decorator(csrf_exempt, name="dispatch")
class FileDownloadView(View):
    def __process_download(self, request):
        try:
            gc_no = request.GET['gc_no']
            fname = request.GET['fname']
            datetime = request.GET['datetime']
            filename = request.GET['filename']

            file_path = f"{MEDIA_ROOT}/{gc_no}/{fname}/{datetime}/{filename}"

            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="image/jpeg")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
            else:
                result = {'rCode': 400, 'rMessage': "Bad request"}
                return JsonResponse(result, safe=False)

        except Exception as ex:
            result = {'rCode': 500, 'rMessage': str(ex)}
            return JsonResponse(result, safe=False)

    def __process_static_image(self, request):
        try:
            file_name = request.GET["file_name"]

            file_path = f"{GPS_SCORE_APP_STATIC_ROOT}/image/{file_name}"

            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="image/jpeg")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
            else:
                result = {'rCode': 400, 'rMessage': "Bad request"}
                return JsonResponse(result, safe=False)

        except Exception as ex:
            result = {'rCode': 500, 'rMessage': str(ex)}
            return JsonResponse(result, safe=False)

    def __process_gps_score_image(self, request):
        try:
            co_div = request.GET["co_div"]
            game_sid = request.GET["game_sid"]
            date_time = request.GET["datetime"]
            file_name = request.GET["filename"]

            file_path = f"{MEDIA_ROOT}/{co_div}/{game_sid}/{date_time}/{file_name}"

            if os.path.exists(file_path):
                with open(file_path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="image/jpeg")
                    response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                    return response
            else:
                result = {'rCode': 400, 'rMessage': "Bad request"}
                return JsonResponse(result, safe=False)

        except Exception as ex:
            result = {'rCode': 500, 'rMessage': str(ex)}
            return JsonResponse(result, safe=False)

    def get(self, request, *args, **kwargs):
        if kwargs["param"] == "download":
            return self.__process_download(request=request)
        elif kwargs["param"] == "static-image":
            return self.__process_static_image(request=request)
        elif kwargs["param"] == "gps-score-image":
            return self.__process_gps_score_image(request=request)

import os
import sys
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.template.loader import get_template
import socket
import imgkit

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

from Commons.common import *

wkhtml_to_image = os.path.join(
    settings.BASE_DIR, "gps_score_app/wkhtmltoimage.exe")


def html_to_image(request):
    template_path = 'gps_score_app/image_template.html'
    template = get_template(template_path)

    context = {"name": "Areeba Seher"}
    html = template.render(context)

    config = imgkit.config(wkhtmltoimage=wkhtml_to_image, xvfb='/opt/bin/xvfb-run')

    image = imgkit.from_string(html, False, config=config)

    # Generate download
    response = HttpResponse(image, content_type='image/jpeg')

    response['Content-Disposition'] = 'attachment; filename=image.jpg'
    # print(response.status_code)
    if response.status_code != 200:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

import os
import sys

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.conf import settings
from .singleton_object import SingletonObject
import imgkit


@method_decorator(csrf_exempt, name="dispatch")
class DisplayGPSScoreView(TemplateView):
    template_name = "gps_score_app/display.html"
    qeuryset = None

    def get_gps_score_data(self, co_div, game_sid):
        hole_par_A_data_list = SingletonObject.database_service.get_hole_par_data(co_div=co_div, cour_name="OUT")
        hole_par_B_data_list = SingletonObject.database_service.get_hole_par_data(co_div=co_div, cour_name="IN")
        gps_score_data_list = SingletonObject.database_service.get_gps_score_data(
            co_div=co_div,
            game_sid=game_sid)

        total_Par_A = 0
        total_Par_B = 0

        for cnt_num in range(1, 10):
            cnt_str = "PAR_CNT_0" + str(cnt_num)
            par_cnt_A_value = int(hole_par_A_data_list[0][cnt_str])
            par_cnt_B_value = int(hole_par_B_data_list[0][cnt_str])

            total_Par_A = total_Par_A + par_cnt_A_value
            total_Par_B = total_Par_B + par_cnt_B_value

        total_Par = total_Par_A + total_Par_B

        for gps_score_data in gps_score_data_list:
            for cnt_num in range(1, 10):
                cnt_str = "PAR_CNT_0" + str(cnt_num)
                par_cnt_A_value = int(hole_par_A_data_list[0][cnt_str])
                par_cnt_B_value = int(hole_par_B_data_list[0][cnt_str])

                score_A_str = "SCORE_A" + str(cnt_num)
                score_B_str = "SCORE_B" + str(cnt_num)
                calc_score_A_str = "CALC_" + score_A_str
                calc_score_B_str = "CALC_" + score_B_str

                score_A_value = int(gps_score_data_list[0][score_A_str])
                score_B_value = int(gps_score_data_list[0][score_B_str])

                calc_score_A_value = score_A_value - par_cnt_A_value
                calc_score_B_value = score_B_value - par_cnt_B_value
                gps_score_data[calc_score_A_str] = calc_score_A_value
                gps_score_data[calc_score_B_str] = calc_score_B_value

        return hole_par_A_data_list, hole_par_B_data_list, gps_score_data_list, total_Par_A, total_Par_B, total_Par

    def get(self, request, *args, **kwargs):
        if kwargs["param"] == "display":
            try:
                co_div = request.GET["co_div"]
                game_sid = request.GET["game_sid"]

                hole_par_A_data_list, hole_par_B_data_list, gps_score_data_list, total_Par_A, total_Par_B, total_Par = \
                    self.get_gps_score_data(co_div=co_div, game_sid=game_sid)

                context = {
                    'view': self.__class__.__name__,
                    'hole_par_A_data_list': hole_par_A_data_list,
                    'hole_par_B_data_list': hole_par_B_data_list,
                    'gps_score_data_list': gps_score_data_list,
                    'total_Par_A': str(total_Par_A),
                    'total_Par_B': str(total_Par_B),
                    'total_Par': str(total_Par)
                }

                return render(
                    request, 'gps_score_app/display.html', context)

            except Exception as ex:
                print(ex)
                return {'rCode': 500, 'rMessage': str(ex)}

        elif kwargs["param"] == "test":
            try:
                co_div = request.GET["co_div"]
                game_sid = request.GET["game_sid"]

                hole_par_A_data_list, hole_par_B_data_list, gps_score_data_list, total_Par_A, total_Par_B, total_Par = \
                    self.get_gps_score_data(co_div=co_div, game_sid=game_sid)

                context = {
                    'view': self.__class__.__name__,
                    'hole_par_A_data_list': hole_par_A_data_list,
                    'hole_par_B_data_list': hole_par_B_data_list,
                    'gps_score_data_list': gps_score_data_list,
                    'total_Par_A': str(total_Par_A),
                    'total_Par_B': str(total_Par_B),
                    'total_Par': str(total_Par)
                }

                template_path = "gps_score_app/display.html"
                template = get_template(template_path)
                html = template.render(context)

                wkhtml_to_image = os.path.join(
                    settings.BASE_DIR, "gps_score_app/wkhtmltoimage.exe")

                config = imgkit.config(wkhtmltoimage=wkhtml_to_image, xvfb='/opt/bin/xvfb-run')

                image = imgkit.from_string(html, False, config=config)

                # Generate download
                response = HttpResponse(image, content_type='image/jpeg')

                response['Content-Disposition'] = 'attachment; filename=gps-score-image.jpg'

                return response

            except Exception as ex:
                print(ex)
                return {'rCode': 500, 'rMessage': str(ex)}

        elif kwargs["param"] == "pardata":
            try:
                co_div = request.GET["co_div"]
                par_data_list = SingletonObject.database_service.get_par_data(co_div=co_div)

                context = {
                    'view': self.__class__.__name__,
                    'par_data_list': par_data_list
                }

                return render(
                    request, 'gps_score_app/display_par_data.html', context)

            except Exception as ex:
                print(ex)
                return {'rCode': 500, 'rMessage': str(ex)}

        elif kwargs["param"] == "scoredata":
            try:
                co_div = request.GET["co_div"]
                game_sid = request.GET["game_sid"]
                gps_score_data_list = SingletonObject.database_service.get_gps_score_data(
                    co_div=co_div,
                    game_sid=game_sid)

                context = {
                    'view': self.__class__.__name__,
                    'gps_score_data_list': gps_score_data_list
                }

                return render(
                    request, 'gps_score_app/display_gps_score.html', context)

            except Exception as ex:
                print(ex)
                return {'rCode': 500, 'rMessage': str(ex)}

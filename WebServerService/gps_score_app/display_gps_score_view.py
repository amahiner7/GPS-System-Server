from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView
from .singleton_object import SingletonObject
from django.http import HttpResponse, JsonResponse


@method_decorator(csrf_exempt, name="dispatch")
class DisplayGPSScoreView(TemplateView):
    template_name = "gps_score_app/display.html"
    qeuryset = None

    def get(self, request, *args, **kwargs):
        if kwargs["param"] == "display":
            try:

                co_div = request.GET["co_div"]
                game_sid = request.GET["game_sid"]
                hole_par_A_data_list = SingletonObject.database_service.get_hole_par_data(co_div=co_div, cour_name="CO")
                hole_par_B_data_list = SingletonObject.database_service.get_hole_par_data(co_div=co_div, cour_name="CI")

                totoal_A_Par = 0
                totoal_B_Par = 0

                for part_cnt_num in range(1, 9):
                    par_cnt_str = "PAR_CNT_0" + str(part_cnt_num)
                    totoal_A_Par = totoal_A_Par + int(hole_par_A_data_list[0][par_cnt_str])
                    totoal_B_Par = totoal_B_Par + int(hole_par_B_data_list[0][par_cnt_str])

                total_Par = totoal_A_Par + totoal_B_Par

                context = {
                    'view': self.__class__.__name__,
                    'hole_par_A_data_list': hole_par_A_data_list,
                    'hole_par_B_data_list': hole_par_B_data_list,
                    'total_A_Par': str(totoal_A_Par),
                    'total_B_Par': str(totoal_B_Par),
                    'total_Par': str(total_Par),
                }

                return render(
                    request, 'gps_score_app/display.html', context)

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

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .singleton_object import SingletonObject


@method_decorator(csrf_exempt, name="dispatch")
class DisplayGPSScoreView(View):
    def get(self, request, param):
        try:
            if param == "display":
                co_div = request.GET["co_div"]
                game_sid = request.GET["game_sid"]

                print("co_div: ", co_div)
                print("game_sid: ", game_sid)
                par_data_list = SingletonObject.database_service.get_par_data(co_div)

                context = {'par_data_list': par_data_list}

                return render(
                    request, 'gps_score_app/display_gps_score.html', context)
        except Exception as ex:
            print("DisplayGPSScoreView.get():", ex)
            return {'rCode': 500, 'rMessage': str(ex)}

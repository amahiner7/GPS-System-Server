from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .singleton_object import SingletonObject


@method_decorator(csrf_exempt, name="dispatch")
class DisplayGPSScoreView(View):
    def __display(self, request):
        try:
            co_div = request.GET["co_div"]
            game_sid = request.GET["game_sid"]

            print("co_div: ", co_div)
            print("game_sid: ", game_sid)
            par_data_list = SingletonObject.database_service.get_par_data(co_div)

            context = {'par_data_list': par_data_list}

            return render(
                request, 'gps_score_app/display_par_data.html', context)
        except Exception as ex:
            print("DisplayGPSScoreView.__display():", ex)
            return {'rCode': 500, 'rMessage': str(ex)}

    def __display_par_data(self, request):
        try:
            co_div = request.GET["co_div"]

            par_data_list = SingletonObject.database_service.get_par_data(co_div)

            context = {'par_data_list': par_data_list}

            return render(
                request, 'gps_score_app/display_par_data.html', context)
        except Exception as ex:
            print("DisplayGPSScoreView.__display_par_data():", ex)
            return {'rCode': 500, 'rMessage': str(ex)}

    def __display_gps_score(self, request):
        try:
            co_div = request.GET["co_div"]
            game_sid = request.GET["game_sid"]

            par_data_list = SingletonObject.database_service.get_par_data(co_div)

            context = {'par_data_list': par_data_list}

            return render(
                request, 'gps_score_app/display_gps_score.html', context)
        except Exception as ex:
            print("DisplayGPSScoreView.__display_gps_score():", ex)
            return {'rCode': 500, 'rMessage': str(ex)}

    def get(self, request, param):
        if param == "display":
            self.__display(request)
        if param == "par_data":
            self.__display_par_data(request)
        elif param == "gps_score":
            self.__display_gps_score(request)


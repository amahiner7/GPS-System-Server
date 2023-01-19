from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .singleton_object import SingletonObject
from django.http import HttpResponse, JsonResponse

@method_decorator(csrf_exempt, name="dispatch")
class DisplayGPSScoreView(View):
    # @csrf_exempt
    # def __display(self, request):
    #     try:
    #         co_div = request.GET["co_div"]
    #         game_sid = request.GET["game_sid"]
    #
    #         print("co_div: ", co_div)
    #         print("game_sid: ", game_sid)
    #         par_data_list = SingletonObject.database_service.get_par_data(co_div)
    #
    #         context = {'par_data_list': par_data_list}
    #         return JsonResponse(context, safe=False)
    #         # return render(
    #         #     request, 'gps_score_app/display_par_data.html', context)
    #     except Exception as ex:
    #         print("DisplayGPSScoreView.__display():", ex)
    #         return {'rCode': 500, 'rMessage': str(ex)}
    #
    # @csrf_exempt
    # def __display_par_data(self, request):
    #     try:
    #         co_div = request.GET["co_div"]
    #
    #         par_data_list = SingletonObject.database_service.get_par_data(co_div)
    #
    #         context = {'par_data_list': par_data_list}
    #         return render(
    #             request, 'gps_score_app/display_par_data.html', context)
    #     except Exception as ex:
    #         print("DisplayGPSScoreView.__display_par_data():", ex)
    #         return {'rCode': 500, 'rMessage': str(ex)}
    #
    # @csrf_exempt
    # def __display_gps_score(self, request):
    #     try:
    #         co_div = request.GET["co_div"]
    #         game_sid = request.GET["game_sid"]
    #
    #         par_data_list = SingletonObject.database_service.get_par_data(co_div)
    #
    #         context = {'par_data_list': par_data_list}
    #
    #         return render(
    #             request, 'gps_score_app/display_gps_score.html', context)
    #     except Exception as ex:
    #         print("DisplayGPSScoreView.__display_gps_score():", ex)
    #         return {'rCode': 500, 'rMessage': str(ex)}

    def get(self, request, param):
        if param == "display":
            pass
        if param == "par_data":
            try:
                co_div = request.GET["co_div"]

                par_data_list = SingletonObject.database_service.get_par_data(co_div=co_div)

                context = {'par_data_list': par_data_list}
                return render(
                    request, 'gps_score_app/display_par_data.html', context)
            except Exception as ex:
                print("DisplayGPSScoreView.__display_par_data():", ex)
                return {'rCode': 500, 'rMessage': str(ex)}
        elif param == "gps_score":
            try:
                co_div = request.GET["co_div"]
                game_sid = request.GET["game_sid"]

                gps_score_data_list = SingletonObject.database_service.get_gps_score_data(
                    co_div=co_div,
                    game_sid=game_sid)

                context = {'gps_score_data_list': gps_score_data_list}

                return render(
                    request, 'gps_score_app/display_gps_score.html', context)
            except Exception as ex:
                print("DisplayGPSScoreView.__display_gps_score():", ex)
                return {'rCode': 500, 'rMessage': str(ex)}


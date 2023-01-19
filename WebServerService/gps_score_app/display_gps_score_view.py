from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .singleton_object import SingletonObject


@method_decorator(csrf_exempt, name="dispatch")
class DisplayGPSScoreView(View):
    def get(self, request):

        print("Database status: ", SingletonObject.database_service.is_connected())
        # file_information = FileInformation.objects.all()
        context = {'information': "This is test body."}

        return render(
            request, 'gps_score_app/display_gps_score.html', context)

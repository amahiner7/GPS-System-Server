from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import FileInformation


@method_decorator(csrf_exempt, name="dispatch")
class FileListView(View):
    def get(self, request):
        file_information = FileInformation.objects.all()
        context = {'file_information': file_information}

        return render(
            request, 'fileupload/filelist.html', context)

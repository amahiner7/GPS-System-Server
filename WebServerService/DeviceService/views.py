from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from .forms import FileUploadForm
# from .forms import ProductForm
from .models import FileUpload

def index(request):
    return HttpResponse("Hello, World. You're at the Device index.")


def fileupload(request):
    if request.method == "GET":
        fileuploadForm = FileUploadForm
        context = \
        {
            'fileuploadForm': fileuploadForm,
        }
        return render(request, 'DeviceService/fileupload.html', context)

    elif request.method == 'POST':
        title = request.POST['title']
        imgfile = request.FILES["imgfile"]
        fileupload = FileUpload(
            title=title,
            imgfile=imgfile,
        )
        fileupload.save()

        result = {"rCode": "0", "rMessage": "Success"}
        return JsonResponse(result, safe=False)


# def product_create(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)  # 꼭 !!!! files는 따로 request의 FILES로 속성을 지정해줘야 함
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.author = request.user
#             product.detailfunc = product.detailfunc.replace("'", "").replace("[", "").replace("]", "")
#             product.save()
#             return redirect('sales:index')
#     else:
#         form = ProductForm()  # request.method 가 'GET'인 경우
#     context = {'form': form}
#     return render(request, 'sales/product_form.html', context)



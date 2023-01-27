from django import forms
from .models import FileInformation


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileInformation

        fields = ['gc_no', 'fname', 'toUpFile']
        labels = \
            {
                'gc_no': '업장 코드',
                'fname': '폴더 이름',
                'toUpFile': '업로드 파일'
            }

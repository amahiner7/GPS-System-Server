from django import forms
from .models import FileUpload


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload

        fields = ['title', 'imgfile']
        labels = \
            {
                'title': 'Title',
                'imgfile': 'Image File'
            }

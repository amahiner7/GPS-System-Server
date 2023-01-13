from django import forms
from .models import FileInformation


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileInformation

        fields = ['title', 'image_file']
        labels = \
            {
                'title': 'Title',
                'image_file': 'Image File'
            }

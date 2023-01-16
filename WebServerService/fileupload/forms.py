from django import forms
from .models import FileInformation


class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileInformation

        fields = ['image']
        labels = \
            {
                'image': 'Image File'
            }

from django import forms
from .models import ImagemUpload

class UploadCSVForm(forms.Form):
    arquivo = forms.FileField(
        label='Selecione o arquivo CSV',
        widget=forms.ClearableFileInput(
            attrs={
                'class': 'block w-full text-sm text-gray-700 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }
        )
    )

class ImagemUploadForm(forms.ModelForm):
    class Meta:
        model = ImagemUpload
        fields = ['imagem']

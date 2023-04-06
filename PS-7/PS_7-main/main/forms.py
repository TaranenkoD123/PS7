from .models import Img
from django.forms import ModelForm


class ImgForm(ModelForm):
    class Meta:
        model = Img
        fields = ['img',]

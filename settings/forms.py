from django.forms import ModelForm

from .models import Branch, MapConfig


class BranchAddForm(ModelForm):
    class Meta:
        model = Branch
        fields = '__all__'

class MapForm(ModelForm):
    class Meta:
        model = MapConfig
        fields = '__all__'
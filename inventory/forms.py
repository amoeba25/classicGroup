from django.forms import ModelForm

from .models import RawInventory, FinishedInventory, UtilityInventory


class rawAddForm(ModelForm):
    class Meta:
        model = RawInventory
        fields = '__all__'


class finishedAddForm(ModelForm):
    class Meta:
        model = FinishedInventory
        fields = '__all__'


class utilityAddForm(ModelForm):
    class Meta:
        model = UtilityInventory
        fields = '__all__'

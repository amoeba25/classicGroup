from django.forms import ModelForm, inlineformset_factory
from .models import ProductionPlant, Batch


class ProductionForm(ModelForm):
    class Meta:
        model = ProductionPlant
        fields = '__all__'


class BatchForm(ModelForm):
    class Meta:
        model = Batch
        fields = '__all__'
        

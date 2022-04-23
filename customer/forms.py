from django.forms import ModelForm

from .models import Customer


class CustomerAddForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

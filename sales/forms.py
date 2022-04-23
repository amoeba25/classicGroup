from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import SalesPlanning, PerformaInvoice, SaleOrder
from inventory.models import TotalInventory


class PlanningForm(ModelForm):
    class Meta:
        model = SalesPlanning
        fields = '__all__'

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['item'].queryset = TotalInventory.objects.none()

        if 'item' in self.data:
            self.fields['item'].queryset = TotalInventory.objects.all()
        elif self.instance.pk:
            try:
                self.fields['item'].queryset = TotalInventory.objects.filter(select_branch=self.instance.select_branch)
            except:
                pass


class PerformaBasicForm(ModelForm):
    class Meta:
        model = PerformaInvoice
        fields = '__all__'


class SalesOrderForm(ModelForm):
    class Meta:
        model = SaleOrder
        fields = '__all__'
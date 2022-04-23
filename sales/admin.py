from django.contrib import admin

# Register your models here.
from .models import SalesPlanning, PerformaInvoice

admin.site.register(SalesPlanning)
admin.site.register(PerformaInvoice)

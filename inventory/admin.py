from django.contrib import admin

# Register your models here.
from .models import RawInventory, FinishedInventory, UtilityInventory, TotalInventory

admin.site.register(RawInventory)
admin.site.register(FinishedInventory)
admin.site.register(UtilityInventory)
admin.site.register(TotalInventory)
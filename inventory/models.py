import uuid

from django.db import models
from settings.models import Branch


# Create your models here.
class RawInventory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    select_branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    slug = models.CharField(max_length=40, unique=True, null=True, default=None)
    quantity = models.IntegerField()
    reserved_qt = models.IntegerField()
    max_quantity = models.IntegerField()
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.product_name + " " + self.slug

    class Meta:
        verbose_name_plural = "Raw Inventory"

    @property
    def available_quantity(self):
        available_quantity = int(self.quantity) - int(self.reserved_qt)
        return available_quantity


class FinishedInventory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    select_branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    slug = models.CharField(max_length=40, unique=True, null=True, default=None)
    quantity = models.IntegerField()
    reserved_qt = models.IntegerField()
    max_quantity = models.IntegerField()
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.product_name + " " + self.slug

    class Meta:
        verbose_name_plural = "Finished Inventory"

    @property
    def available_quantity(self):
        available_quantity = self.quantity - self.reserved_qt
        return available_quantity


class UtilityInventory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    select_branch = models.ForeignKey(Branch, null=True, blank=True, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    slug = models.CharField(max_length=40, unique=True, null=True, default=None)
    quantity = models.IntegerField()
    reserved_qt = models.IntegerField()
    max_quantity = models.IntegerField()
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.product_name + " " + self.slug

    class Meta:
        verbose_name_plural = "Utility Inventory"

    @property
    def available_quantity(self):
        available_quantity = self.quantity - self.reserved_qt
        return available_quantity


class TotalInventory(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    select_branch = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    unique_name = models.CharField(max_length=100)
    quantity = models.CharField(max_length=100)
    reserved_qt = models.CharField(max_length=100)
    max_quantity = models.CharField(max_length=100)
    available_quantity = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.product_name + ' ' + self.unique_name

    class Meta:
        verbose_name_plural = "Total Inventory"

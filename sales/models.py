from django.db import models
import uuid
from inventory.models import TotalInventory
from settings.models import Branch
from customer.models import Customer


# Create your models here.
class SalesPlanning(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    select_branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    item = models.ForeignKey(TotalInventory, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=100)
    reserved_qt = models.CharField(max_length=100)
    available_quantity = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customer_quantity = models.CharField(max_length=100)
    destination_add = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=12)
    loggedIn = models.CharField(max_length=30)
    remarks = models.CharField(max_length=1000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return str(self.item) + ' ' + str(self.customer)

    class Meta:
        verbose_name_plural = 'Sales Planning'


class PerformaInvoice(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    piNo = models.CharField(max_length=100)
    date = models.DateField()
    selectCustomer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    gstNo = models.CharField(max_length=30, null=True, blank=True)
    contactPerson = models.CharField(max_length=100, null=True, blank=True)
    phonePerson = models.CharField(max_length=13, null=True, blank=True)
    deliveryAdd = models.CharField(max_length=100, null=True, blank=True)
    emailId = models.CharField(max_length=100, null=True, blank=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)
    select_branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    product = models.ForeignKey(TotalInventory, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=20, null=True, blank=True)
    price = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return str(self.piNo) + " " + self.selectCustomer.customer_name

    class Meta:
        verbose_name_plural = 'Performa Invoice Basic'


class SaleOrder(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    saleNo = models.CharField(max_length=100)
    date = models.DateField()
    piRef = models.ForeignKey(PerformaInvoice, on_delete=models.CASCADE)
    selectCustomer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    gstNo = models.CharField(max_length=30, null=True, blank=True)
    contactPerson = models.CharField(max_length=100, null=True, blank=True)
    phonePerson = models.CharField(max_length=13, null=True, blank=True)
    emailId = models.CharField(max_length=100, null=True, blank=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)
    loadingFrom = models.ForeignKey(Branch, on_delete=models.CASCADE)
    deliveryAt = models.CharField(max_length=100, null=True, blank=True)
    creditNo = models.CharField(max_length=100, null=True, blank=True)
    paymentTerms = models.CharField(max_length=100, null=True, blank=True)
    freight = models.CharField(max_length=100, null=True, blank=True)
    transportDetails = models.CharField(max_length=100, null=True, blank=True)
    product = models.ForeignKey(TotalInventory, on_delete=models.CASCADE)
    quantity = models.CharField(max_length=20, null=True, blank=True)
    price = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.saleNo + '' + str(self.selectCustomer.customer_name)

    class Meta:
        verbose_name_plural = 'Sales Order'


class SaleStatus(models.Model):
    choices = (
        ("Approve", "Approve"),
        ("Dis-Approve", "Dis-Approve"),
        ("Dispatch", "Dispatch"),
        ("Delivered", "Delivered")
    )
    saleNo = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=choices, default="Reserved")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
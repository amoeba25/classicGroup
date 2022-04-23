from django.db import models
import uuid

# Create your models here.

class Customer(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    customer_type = models.CharField(max_length=100, null=True,blank=True)
    customer_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100)
    billing_address = models.CharField(max_length=200)
    shipping_address = models.CharField(max_length=200)
    reference = models.CharField(max_length=100)
    gst_no = models.CharField(max_length=100)
    payment_terms = models.CharField(max_length=100)
    delivery_terms = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.customer_name
    
    class Meta:
        verbose_name_plural = "Customer"

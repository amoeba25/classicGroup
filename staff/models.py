import uuid

from django.contrib.auth.models import Permission
from django.contrib.auth.models import User
from django.db import models
from settings.models import Branch

# Create your models here.
def permission_string_method(self):
    return '%s' % self.name


Permission.__str__ = permission_string_method


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=50, null=True, blank=True)
    linkedIn_link = models.CharField(max_length=100, null=True, blank=True)
    aadhar_No = models.CharField(max_length=30, null=True, blank=True)
    pan_card = models.CharField(max_length=50, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = "Profile"
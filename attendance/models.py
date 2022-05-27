from pickle import NONE
from django.db import models
from django.contrib.auth.models import User
import datetime
import uuid

# Create your models here.
class Attendance(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, to_field="username", on_delete= models.CASCADE)
    date = models.DateField(null= True, blank= True)
    time_in = models.TimeField(null= True, blank=True)
    time_out = models.TimeField(null= True, blank= True)
    
    def __str__(self):
        return f"Attendance {self.user}"
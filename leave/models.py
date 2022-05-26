from django.db import models
from django.contrib.auth.models import User
import uuid
import datetime

# Create your models here.
class LeaveApp(models.Model):
    choices = (
        ("Pending", "Pending"),
        ("Approve", "Approve"),
        ("Rejected", "Rejected"),
    )
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, to_field="username", on_delete= models.CASCADE)
    title = models.CharField(max_length= 100)
    body = models.TextField()
    leave_date = models.DateField(("Date"), default=datetime.date.today) # date for applying leave
    status = models.CharField(max_length=30, choices=choices, default=choices[0][0]) # status of the application
    
    def __str__(self):
        return str(self.user) + 'leave_app'
    
    
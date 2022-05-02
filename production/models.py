from django.db import models
import uuid
from settings.models import Branch


# Create your models here.
class ProductionPlant(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    machine = models.CharField(max_length=50) 
    date = models.DateField()
    grade = models.CharField(max_length=50)
    
    
#every batch can have onyl one machine for it
class Batch(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    production_plant = models.ForeignKey(ProductionPlant, on_delete= models.CASCADE)
    batch_no = models.IntegerField() 
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    drum_fill = models.IntegerField()
    batch_hours = models.IntegerField()
    total_time = models.IntegerField()
    
    def __str__():
        return str(self.batch_no)
    

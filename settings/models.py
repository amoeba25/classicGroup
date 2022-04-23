import uuid
from django.db import models


class Branch(models.Model):
    regionNameChoice = (
        ('North', 'North Zone'),
        ('East', 'East Zone'),
        ('West', 'West Zone'),
        ('South', 'South Zone')
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    regionName = models.CharField(max_length=10, choices=regionNameChoice)
    stateName = models.CharField(max_length=20, null=True)
    cityName = models.CharField(max_length=20, null=True)
    branchCode = models.CharField(max_length=10, null=True)
    branchName = models.CharField(max_length=100, null=True)
    branchAddress1 = models.CharField(max_length=100, null=True)
    branchAddress2 = models.CharField(max_length=100, null=True)
    zip_code = models.IntegerField(blank=True, null=True)
    branchNumber = models.CharField(max_length=100, null=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True, default='0')
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, blank=True, null=True, default='0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.branchName

    class Meta:
        verbose_name_plural = "Branch"


class MapConfig(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    google_map_api = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.google_map_api

    class Meta:
        verbose_name_plural = "Google Map API Key"


from django.db import models
from owner.models import Owner
from vehicle.models import Vehicle

# Create your models here.
class ViolationHistory(models.Model):
    description = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    fee = models.FloatField(default=5000000)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='violation/')

class UnsureViolationHistory(models.Model):
    description = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True, blank=True, upload_to='unsureviolation/')
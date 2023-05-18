from django.db import models
from owner.models import Owner
# Create your models here.
class Vehicle(models.Model):
    plate = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self) -> str:
        return self.plate
from django.db import models

# Create your models here.
class Owner(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)
    id_card = models.CharField(max_length=20)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    def __str__(self):
        return self.firstname + " " + self.lastname
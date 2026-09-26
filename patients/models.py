from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name
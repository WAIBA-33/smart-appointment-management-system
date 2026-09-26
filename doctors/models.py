from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    working_start = models.TimeField()
    working_end = models.TimeField()

    def __str__(self):
        return self.name
    
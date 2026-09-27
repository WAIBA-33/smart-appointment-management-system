from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=200)

    def clean(self):
        if self.date_of_birth and self.date_of_birth > timezone.localdate():
            raise ValidationError({
                'date_of_birth': 'Date of birth cannot be in the future.'
            })

    def __str__(self):
        return self.name
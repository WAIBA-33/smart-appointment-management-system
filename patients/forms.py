from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Patient


class PatientSignupForm(UserCreationForm):

    name = forms.CharField(
        max_length=100,
        required=True,
        label="Full Name"
    )

    phone = forms.CharField(
        max_length=20,
        required=True,
        label="Phone"
    )

    date_of_birth = forms.DateField(
        required=True,
        label="Date of Birth",
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "form-control"
            }
        )
    )

    address = forms.CharField(
        max_length=200,
        required=True,
        label="Address"
    )

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
        ]

    def clean_name(self):
        name = self.cleaned_data["name"].strip()

        if len(name) < 2:
            raise forms.ValidationError(
                "Name must contain at least 2 characters."
            )

        if not all(char.isalpha() or char.isspace() for char in name):
            raise forms.ValidationError(
                "Name can contain only letters and spaces."
            )

        return name

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()

        if not phone.isdigit():
            raise forms.ValidationError(
                "Phone number must contain only digits."
            )

        if len(phone) != 10:
            raise forms.ValidationError(
                "Phone number must contain exactly 10 digits."
            )

        return phone

    def clean_date_of_birth(self):
        dob = self.cleaned_data["date_of_birth"]

        if dob > date.today():
            raise forms.ValidationError(
                "Date of birth cannot be in the future."
            )

        return dob

    def clean_address(self):
        address = self.cleaned_data["address"].strip()

        if len(address) < 3:
            raise forms.ValidationError(
                "Address must contain at least 3 characters."
            )

        return address
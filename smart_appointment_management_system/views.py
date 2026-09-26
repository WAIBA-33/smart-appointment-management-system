from django.shortcuts import render
from doctors.models import Doctor


def home(request):
    doctors = Doctor.objects.all()

    return render(
        request,
        "home.html",
        {
            "doctors": doctors,
        }
    )
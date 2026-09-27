from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import PatientSignupForm
from .models import Patient


def patient_signup(request):

    if request.method == "POST":

        form = PatientSignupForm(request.POST)

        if form.is_valid():

            user = form.save()

            Patient.objects.create(
                user=user,
                name=form.cleaned_data["name"],
                phone=form.cleaned_data["phone"],
                date_of_birth=form.cleaned_data["date_of_birth"],
                address=form.cleaned_data["address"],
            )

            patients_group = Group.objects.get(
                name="Patients"
            )

            user.groups.add(patients_group)

            login(request, user)

            messages.success(
                request,
                "Your patient account has been created successfully."
            )

            return redirect("accounts:role_redirect")

    else:

        form = PatientSignupForm()

    return render(
        request,
        "patients/signup.html",
        {
            "form": form,
        }
    )


@login_required
def patient_dashboard(request):

    patient = Patient.objects.get(
        user=request.user
    )

    return render(
        request,
        "patients/dashboard.html",
        {
            "patient": patient,
        }
    )
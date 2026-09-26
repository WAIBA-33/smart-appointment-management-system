from django.urls import path
from . import views

app_name = "patients"

urlpatterns = [

    path(
        "signup/",
        views.patient_signup,
        name="patient_signup",
    ),

    path(
        "dashboard/",
        views.patient_dashboard,
        name="patient_dashboard",
    ),

]
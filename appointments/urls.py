from django.urls import path
from . import views

app_name = "appointments"

urlpatterns = [

    path(
        "create/",
        views.appointment_create,
        name="appointment_create",
    ),

    path(
        "my-appointments/",
        views.my_appointments,
        name="my_appointments",
    ),

    path(
        "doctor-dashboard/",
        views.doctor_dashboard,
        name="doctor_dashboard",
    ),

    path(
        "update-status/<int:appointment_id>/",
        views.update_appointment_status,
        name="update_appointment_status",
    ),

    path(
        "cancel/<int:appointment_id>/",
        views.cancel_appointment,
        name="cancel_appointment",
    ),

    path(
    "reschedule/<int:appointment_id>/",
    views.reschedule_appointment,
    name="reschedule_appointment",
    ),

    path(
    "doctor-categories/",
    views.doctor_categories,
    name="doctor_categories",
    ),

]


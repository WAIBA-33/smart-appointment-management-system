from datetime import date, datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from doctors.models import Doctor
from patients.models import Patient
from .models import Appointment
from .services import get_available_slots


@login_required
def appointment_create(request):

    # Only patients can access the booking page
    if not Patient.objects.filter(user=request.user).exists():

        messages.error(
            request,
            "Only patients can book appointments."
        )

        return redirect("appointments:doctor_dashboard")

    doctors = Doctor.objects.all()
    available_slots = []

    selected_doctor = None
    selected_date = None

    if request.method == "POST":

        doctor_id = request.POST.get("doctor")
        date_value = request.POST.get("appointment_date")
        time_value = request.POST.get("appointment_time")

        if doctor_id and date_value:

            selected_doctor = Doctor.objects.get(
                id=doctor_id
            )

            selected_date = date.fromisoformat(
                date_value
            )

            # Prevent booking appointments in the past
            if selected_date < date.today():

                messages.error(
                    request,
                    "You cannot book an appointment for a past date."
                )

                return redirect(
                    "appointments:appointment_create"
                )

            available_slots = get_available_slots(
                selected_doctor,
                selected_date
            )

        # Create appointment when a time is selected
        if doctor_id and date_value and time_value:

            patient = Patient.objects.get(
                user=request.user
            )

            appointment_time = datetime.strptime(
                time_value,
                "%H:%M:%S"
            ).time()

            # Check if the selected slot is already booked
            slot_taken = Appointment.objects.filter(
                doctor=selected_doctor,
                appointment_date=selected_date,
                appointment_time=appointment_time,
                status__in=["Pending", "Confirmed"]
            ).exists()

            if slot_taken:

                messages.error(
                    request,
                    "Sorry, this appointment slot is already booked."
                )

                return redirect(
                    "appointments:appointment_create"
                )

            # Create the appointment
            Appointment.objects.create(
                patient=patient,
                doctor=selected_doctor,
                appointment_date=selected_date,
                appointment_time=appointment_time,
                reason="General appointment"
            )

            messages.success(
                request,
                f"Appointment booked successfully with "
                f"{selected_doctor.name} on {selected_date} "
                f"at {appointment_time.strftime('%I:%M %p')}."
            )

            return redirect(
                "appointments:appointment_create"
            )

    context = {
        "doctors": doctors,
        "available_slots": available_slots,
        "selected_doctor": selected_doctor,
        "selected_date": selected_date,
    }

    return render(
        request,
        "appointments/appointment_create.html",
        context
    )


@login_required
def my_appointments(request):

    # Only patients can view their appointments
    if not Patient.objects.filter(user=request.user).exists():

        messages.error(
            request,
            "Only patients can view their appointments."
        )

        return redirect(
            "appointments:doctor_dashboard"
        )

    patient = Patient.objects.get(
        user=request.user
    )

    appointments = Appointment.objects.filter(
        patient=patient
    ).order_by(
        "-appointment_date",
        "-appointment_time"
    )

    return render(
        request,
        "appointments/my_appointments.html",
        {
            "appointments": appointments
        }
    )


@login_required
def doctor_dashboard(request):

    if not Doctor.objects.filter(user=request.user).exists():

        messages.error(
            request,
            "Only doctors can access the doctor dashboard."
        )

        return redirect(
            "appointments:appointment_create"
        )

    doctor = Doctor.objects.get(
        user=request.user
    )

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).order_by(
        "appointment_date",
        "appointment_time"
    )

    return render(
        request,
        "appointments/doctor_dashboard.html",
        {
            "appointments": appointments,
            "doctor": doctor,
        }
    )


@login_required
def update_appointment_status(
    request,
    appointment_id
):

    # Only doctors can update appointment status
    if not Doctor.objects.filter(user=request.user).exists():

        messages.error(
            request,
            "Only doctors can update appointment status."
        )

        return redirect(
            "appointments:appointment_create"
        )

    doctor = Doctor.objects.get(
        user=request.user
    )

    appointment = Appointment.objects.get(
        id=appointment_id
    )

    # Make sure this appointment belongs to the logged-in doctor
    if appointment.doctor != doctor:

        messages.error(
            request,
            "You are not authorized to update this appointment."
        )

        return redirect(
            "appointments:doctor_dashboard"
        )

    if request.method == "POST":

        new_status = request.POST.get("status")

        if new_status in [
            "Confirmed",
            "Completed",
            "Cancelled"
        ]:

            appointment.status = new_status
            appointment.save()

        return redirect(
            "appointments:doctor_dashboard"
        )

    return redirect(
        "appointments:doctor_dashboard"
    )


@login_required
def cancel_appointment(request, appointment_id):

    # Only patients can cancel appointments
    if not Patient.objects.filter(user=request.user).exists():

        messages.error(
            request,
            "Only patients can cancel appointments."
        )

        return redirect(
            "appointments:doctor_dashboard"
        )

    patient = Patient.objects.get(
        user=request.user
    )

    appointment = Appointment.objects.get(
        id=appointment_id
    )

    # Make sure this appointment belongs to the logged-in patient
    if appointment.patient != patient:

        messages.error(
            request,
            "You are not authorized to cancel this appointment."
        )

        return redirect(
            "appointments:my_appointments"
        )

    # Only Pending and Confirmed appointments can be cancelled
    if appointment.status not in [
        "Pending",
        "Confirmed"
    ]:

        messages.error(
            request,
            "This appointment cannot be cancelled."
        )

        return redirect(
            "appointments:my_appointments"
        )

    if request.method == "POST":

        appointment.status = "Cancelled"
        appointment.save()

        messages.success(
            request,
            "Your appointment has been cancelled successfully."
        )

    return redirect(
        "appointments:my_appointments"
    )


@login_required
def reschedule_appointment(request, appointment_id):

    # Only patients can reschedule appointments
    if not Patient.objects.filter(user=request.user).exists():

        messages.error(
            request,
            "Only patients can reschedule appointments."
        )

        return redirect(
            "appointments:doctor_dashboard"
        )

    patient = Patient.objects.get(
        user=request.user
    )

    appointment = Appointment.objects.get(
        id=appointment_id
    )

    # Make sure this appointment belongs to the logged-in patient
    if appointment.patient != patient:

        messages.error(
            request,
            "You are not authorized to reschedule this appointment."
        )

        return redirect(
            "appointments:my_appointments"
        )

    # Only Pending and Confirmed appointments can be rescheduled
    if appointment.status not in [
        "Pending",
        "Confirmed"
    ]:

        messages.error(
            request,
            "This appointment cannot be rescheduled."
        )

        return redirect(
            "appointments:my_appointments"
        )

    available_slots = []
    selected_date = appointment.appointment_date

    if request.method == "POST":

        date_value = request.POST.get(
            "appointment_date"
        )

        time_value = request.POST.get(
            "appointment_time"
        )

        if date_value:

            selected_date = date.fromisoformat(
                date_value
            )

            # Prevent selecting a past date
            if selected_date < date.today():

                messages.error(
                    request,
                    "You cannot select a past date."
                )

                return redirect(
                    "appointments:reschedule_appointment",
                    appointment_id=appointment.id
                )

            available_slots = get_available_slots(
                appointment.doctor,
                selected_date
            )

        if date_value and time_value:

            new_time = datetime.strptime(
                time_value,
                "%H:%M:%S"
            ).time()

            # Check whether another active appointment
            # already occupies the selected slot
            slot_taken = Appointment.objects.filter(
                doctor=appointment.doctor,
                appointment_date=selected_date,
                appointment_time=new_time,
                status__in=["Pending", "Confirmed"]
            ).exclude(
                id=appointment.id
            ).exists()

            if slot_taken:

                messages.error(
                    request,
                    "Sorry, this appointment slot is already booked."
                )

                return redirect(
                    "appointments:reschedule_appointment",
                    appointment_id=appointment.id
                )

            # Update the existing appointment
            appointment.appointment_date = selected_date
            appointment.appointment_time = new_time
            appointment.save()

            messages.success(
                request,
                "Your appointment has been rescheduled successfully."
            )

            return redirect(
                "appointments:my_appointments"
            )

    else:

        available_slots = get_available_slots(
            appointment.doctor,
            selected_date
        )

    return render(
        request,
        "appointments/reschedule_appointment.html",
        {
            "appointment": appointment,
            "available_slots": available_slots,
            "selected_date": selected_date,
        }
    )
from datetime import datetime, timedelta

from .models import Appointment


def get_available_slots(doctor, appointment_date):

    appointment_duration = timedelta(minutes=30)

    start_datetime = datetime.combine(
        appointment_date,
        doctor.working_start
    )

    end_datetime = datetime.combine(
        appointment_date,
        doctor.working_end
    )

    booked_slots = set(
    Appointment.objects.filter(
        doctor=doctor,
        appointment_date=appointment_date,
        status__in=['Pending', 'Confirmed']
    ).values_list(
        'appointment_time',
        flat=True
    )
)

    available_slots = []

    current_datetime = start_datetime

    while current_datetime + appointment_duration <= end_datetime:

        current_time = current_datetime.time()

        # Skip slots that are already booked
        if current_time not in booked_slots:

            # Skip time slots that have already passed today
            if (
                appointment_date == datetime.today().date()
                and current_time <= datetime.now().time()
            ):
                current_datetime += appointment_duration
                continue

            available_slots.append(current_time)

        current_datetime += appointment_duration

    return available_slots


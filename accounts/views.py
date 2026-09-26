from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


@login_required
def role_redirect(request):

    if request.user.groups.filter(name="Doctors").exists():
        return redirect("appointments:doctor_dashboard")

    if request.user.groups.filter(name="Patients").exists():
        return redirect("patients:patient_dashboard")

    return redirect("/")


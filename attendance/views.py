from django.core.checks import messages
from django.shortcuts import render, redirect
from datetime import date
from .models import Attendance
from django.db.models import Count, Q

from attendance.models import Attendance
from students.models import ClassRoom
from datetime import date

from django.contrib import messages


def today_attendance(request):
    today = date.today()

    attendance_records = Attendance.objects.filter(
        date=today, student__classroom__teacher=request.user
    ).select_related("student")
    present = attendance_records.filter(status="PRESENT").count()
    absent = attendance_records.filter(status="ABSENT").count()

    context = {
        "attendance_records": attendance_records,
        "today": today,
        "present": present,
        "absent": absent,
    }
    return render(request, "attendance/today_attendance.html", context)


def mark_attendance(request):
    classroom = ClassRoom.objects.filter(teacher=request.user).first()
    if not classroom:
        messages.error(request, "No classroom assigned to you.")
        return redirect("accounts:dashboard")
    students = classroom.students.all()
    if request.method == "POST":
        attendance_date = request.POST.get("date")
        for student in students:
            status = request.POST.get(f"student_{student.id}")
            if not status:
                continue
            Attendance.objects.update_or_create(
                student=student, date=attendance_date, defaults={"status": status}
            )
        messages.success(request, "Attendance saved successfully.")
        return redirect("attendance")
    context = {
        "classroom": classroom,
        "students": students,
        "today": date.today(),
    }
    return render(
        request,
        "attendance/attendance_form.html",
        context,
    )


def attendance_history(request):
    from_date = request.GET.get("from")
    to_date = request.GET.get("to")

    queryset = Attendance.objects.filter(student__classroom__teacher=request.user)

    if from_date:
        queryset = queryset.filter(date__gte=from_date)

    if to_date:
        queryset = queryset.filter(date__lte=to_date)

    attendance_records = (
        queryset.values(
            "date", "student__classroom__name", "student__classroom__section"
        )
        .annotate(
            present_count=Count("id", filter=Q(status="PRESENT")),
            absent_count=Count("id", filter=Q(status="ABSENT")),
        )
        .order_by("-date")
    )

    context = {
        "attendance_records": attendance_records,
        "from_date": from_date,
        "to_date": to_date,
    }

    return render(request, "attendance/attendance_history.html", context)

from django.shortcuts import render
from datetime import date
from .models import Attendance
from django.db.models import Count, Q


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
    return render(request, "attendance/attendance_form.html")


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

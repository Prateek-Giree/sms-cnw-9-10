from django.urls import path

from . import views

urlpatterns = [
    path("list/", views.student, name="student"),
    path("portal/", views.student_lookup, name="student-lookup"),
    path("portal/<int:student_id>/", views.student_dashboard, name="student-dashboard"),
    path("portal/<int:student_id>/marks/", views.student_marks, name="student-marks"),
    path(
        "portal/<int:student_id>/attendance/",
        views.student_attendance,
        name="student-attendance",
    ),
    path(
        "portal/<int:student_id>/report-card/<str:exam_name>/",
        views.student_report_card,
        name="student-report-card",
    ),
]

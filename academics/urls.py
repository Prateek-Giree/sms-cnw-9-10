from django.urls import path
from . import views

urlpatterns = [
    path("assignments/list/", views.assignment_list, name="assignment-list"),
    path("assignments/add/", views.add_assignment, name="add-assignment"),
    path("marks/add/", views.add_marks, name="add-marks"),
    path("marks/view/", views.view_marks, name="view-marks"),
    path("results/", views.student_results, name="student-results"),
    path("report-card/<int:student_id>/<str:exam_name>/", views.report_card, name="report-card"),
]

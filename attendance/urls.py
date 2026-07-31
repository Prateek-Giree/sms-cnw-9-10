from django.urls import path
from . import views
urlpatterns = [
path("list/",views.today_attendance,name="attendance"),
path("mark/",views.mark_attendance,name="mark-attendance"),
path("history/",views.attendance_history,name="attendance-history"),
]

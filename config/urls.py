
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",include('accounts.urls')),
    path("attendance/",include('attendance.urls')),
    path("students/",include('students.urls')),
    path("academics/",include('academics.urls')),
]

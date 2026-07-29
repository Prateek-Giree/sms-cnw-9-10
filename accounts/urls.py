from django.urls import path
from . import views
urlpatterns = [
    path("", views.teacher_login, name="login"),
    path("accounts/logout/", views.teacher_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
]

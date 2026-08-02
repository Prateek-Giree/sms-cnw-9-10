from django.urls import path
from . import views
urlpatterns = [
    path("assignments/list/", views.assignments_list, name="assignment-list"),
    path("assignments/add/", views.add_assignment, name="add-assignment"),
]

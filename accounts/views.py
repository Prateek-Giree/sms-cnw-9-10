from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from students.models import ClassRoom
from django.contrib import messages
from academics.models import Subject


def teacher_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user and user.role == "TEACHER":
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")

    return render(request, "accounts/login.html")


def teacher_logout(request):
    logout(request)
    return redirect("login")


@login_required
def dashboard(request):
    classroom = ClassRoom.objects.filter(teacher=request.user).first()

    student_count = 0
    subject_count = 0

    if classroom:
        student_count = classroom.students.count()
        subject_count = Subject.objects.filter(classroom=classroom).count()

    context = {
        "classroom": classroom,
        "student_count": student_count,
        "subject_count": subject_count,
    }
    return render(request, "accounts/dashboard.html", context)

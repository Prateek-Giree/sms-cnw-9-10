from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, render
from academics.models import Assignment, Subject
from students.models import ClassRoom


def add_assignment(request):
    classroom = ClassRoom.objects.filter(teacher=request.user).first()
    if not classroom:
        messages.error(request, "No classroom assigned to you.")
        return redirect("accounts:dashboard")
    subjects = Subject.objects.filter(classroom=classroom)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        subject_id = request.POST.get("subject")
        subject = Subject.objects.get(id=subject_id)
        Assignment.objects.create(
            title=title,
            description=description,
            subject=subject,
            classroom=classroom,
        )
        messages.success(request, "Assignment created successfully.")
        return redirect("assignment-list")
    context = {
        "classroom": classroom,
        "subjects": subjects,
    }
    return render(
        request,
        "academics/assignment_form.html",
        context,
    )


def assignments_list(request):
    assignments = (
        Assignment.objects.filter(classroom__teacher=request.user)
        .select_related("subject", "classroom")
        .order_by("-created_at")
    )
    return render(
        request, "academics/assignment_list.html", {"assignments": assignments}
    )

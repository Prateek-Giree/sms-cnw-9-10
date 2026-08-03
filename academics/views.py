from django.shortcuts import redirect, render
from django.contrib import messages
from .models import Assignment, Subject
from students.models import ClassRoom
from .models import Marks, Subject


def add_assignment(request):
    classroom = ClassRoom.objects.filter(teacher=request.user).first()

    if not classroom:
        messages.error(request, "No Classroom assigned to you")
        return redirect("dashboard")

    subjects = Subject.objects.filter(classroom=classroom)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        subject_id = request.POST.get("subject")

        subject = Subject.objects.get(id=subject_id)
        Assignment.objects.create(
            title=title, description=description, subject=subject, classroom=classroom
        )
        messages.success(request, "Assignment Created Successfully")
        return redirect("assignment-list")
    context = {"classroom": classroom, "subjects": subjects}
    return render(request, "academics/assignment_form.html", context)


def assignment_list(request):
    assignments = (
        Assignment.objects.filter(classroom__teacher=request.user)
        .select_related("subject", "classroom")
        .order_by("-created_at")
    )
    return render(
        request, "academics/assignment_list.html", {"assignments": assignments}
    )


def add_marks(request):
    classroom = ClassRoom.objects.filter(teacher=request.user).first()
    if not classroom:
        messages.error(request, "No Classroom assigned to you")
        return redirect("dashboard")
    students = classroom.students.all()
    subjects = Subject.objects.filter(classroom=classroom)
    if request.method == "POST":
        subject_id = request.POST.get("subject")
        exam_name = request.POST.get("exam_name")

        if not subject_id or not exam_name:
            messages.error(request, "Subject and exam name are required..")
            return redirect("add-marks")

        subject = Subject.objects.get(id=subject_id, classroom=classroom)

        for student in students:
            marks = request.POST.get(f"student_{student.id}")
            if not marks:
                continue
            Marks.objects.update_or_create(
                student=student,
                subject=subject,
                exam_name=exam_name,
                defaults={"marks_obtained": marks},
            )
        messages.success(request, "Marks saved successfully..")
        return redirect("add-marks")

    context = {"classroom": classroom, "students": students, "subjects": subjects}
    return render(request, "academics/marks_form.html", context)


def view_marks(request):
    classroom = ClassRoom.objects.filter(teacher=request.user).first()
    marks = Marks.objects.none()
    subjects = Subject.objects.none()
    exam_name = []
    if classroom:
        subjects = Subject.objects.filter(classroom=classroom)
        marks = (
            Marks.objects.filter(student__classroom=classroom)
            .select_related(
                "student",
                "subject",
            )
            .order_by("student__name")
        )
        subject_id = request.GET.get("subject")
        exam_name = request.GET.get("exam")

        if subject_id:
            marks = marks.filter(subject_id=subject_id)

        if exam_name:
            marks = marks.filter(exam_name=exam_name)

        exam_name = (
            Marks.objects.filter(student__classroom=classroom)
            .values_list("exam_name", flat=True)
            .distinct()
        )
    context = {
        "marks": marks,
        "subjects": subjects,
        "exam_names": exam_name,
        "selected_subject": request.GET.get("subject", ""),
        "selected_exam": request.GET.get("exam", ""),
    }
    return render(request, "academics/marks_list.html", context)

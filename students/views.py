from django.shortcuts import render
from students.models import ClassRoom, Student
from academics.models import Subject

# Create your views here.


def student(request):
    classroom = ClassRoom.objects.filter(teacher=request.user).first()
    student_count = 0
    subject_count = 0

    students = Student.objects.filter(classroom=classroom)

    if classroom:
        student_count = classroom.students.count()
        subject_count = Subject.objects.filter(classroom=classroom).count()

    context = {
        "classroom": classroom,
        "student_count": student_count,
        "subject_count": subject_count,
        "students": students,
    }
    return render(request, "students/student_list.html", context)

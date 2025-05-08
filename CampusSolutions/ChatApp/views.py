from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from Home.models import Students, Faculties, sections

from .models import Faculty_Messages, Student_Messages
from django.utils import timezone
from django.db.models import Q

User = get_user_model()


# Load the assigned faculties for a student
@login_required
def get_faculties(request):
    student = request.user
    student_section = student.section
    section_object = sections.objects.get(section=student_section)
    sec_id = section_object.id
    assigned_faculties = Faculties.objects.filter(section=sec_id)
    # subjects=subjects.objects.filter()
    # faculty_subjects=Faculties.subjects.objects.filter()

    context = {"assigned_faculties": assigned_faculties}
    return render(request, "faculty_list.html", context)


# Load the assigned students for a faculty
@login_required
def get_studentschatapp(request):
    faculty = request.user
    assigned_sections = faculty.section.all()
    assigned_students = []
    for section in assigned_sections:
        students_in_section = Students.objects.filter(section=section)
        assigned_students.extend(students_in_section)
    context = {"assigned_students": assigned_students}
    return render(request, "student_list.html", context)


@login_required()
def message(request, user_id):
    current_user = request.user

    # check for faculty or student
    if request.method == "POST":
        if current_user.is_staff == False:
            faculty = Faculties.objects.get(id=user_id)
            student_id = current_user.id
            content = request.POST.get("content")

            Student_Messages.objects.create(
                student_id=student_id,
                sent_to_faculty_id=faculty.id,
                content=content,
                sent_at=timezone.now(),
            )
        elif current_user.is_staff == True:
            faculty_id = current_user.id
            student_id = user_id
            content = request.POST.get("content")

            Faculty_Messages.objects.create(
                faculty_id=faculty_id,
                sent_to_student_id=student_id,
                content=content,
                sent_at=timezone.now(),
            )

    return render(request, "message_form.html", {"user_id": user_id})


from django.db.models import Q
from itertools import chain
from operator import attrgetter


@login_required
def chatbox(request, user_id):
    current_user = request.user

    messages = []

    if not current_user.is_staff:
        student = current_user
        faculty = get_object_or_404(Faculties, id=user_id)

        sent_msgs = Student_Messages.objects.filter(
            student_id=student.id, sent_to_faculty_id=faculty.id
        )
        received_msgs = Faculty_Messages.objects.filter(
            faculty_id=faculty.id, sent_to_student_id=student.id
        )

        for msg in sent_msgs:
            msg.sender_type = "student"
        for msg in received_msgs:
            msg.sender_type = "faculty"

    else:
        faculty = current_user
        student = get_object_or_404(Students, id=user_id)

        sent_msgs = Faculty_Messages.objects.filter(
            faculty_id=faculty.id, sent_to_student_id=student.id
        )
        received_msgs = Student_Messages.objects.filter(
            student_id=student.id, sent_to_faculty_id=faculty.id
        )

        for msg in sent_msgs:
            msg.sender_type = "faculty"
        for msg in received_msgs:
            msg.sender_type = "student"

    # Combine and sort
    messages = sorted(chain(sent_msgs, received_msgs), key=attrgetter("sent_at"))

    context = {
        "messages": messages,
        "user_id": user_id,
    }
    return render(request, "chatbox.html", context)


from django.http import JsonResponse
from django.core.serializers import serialize
from django.forms.models import model_to_dict


@login_required
def get_messages(request, user_id):
    current_user = request.user

    if not current_user.is_staff:
        student = current_user
        faculty = get_object_or_404(Faculties, id=user_id)
    else:
        faculty = current_user
        student = get_object_or_404(Students, id=user_id)

    sent_msgs = Student_Messages.objects.filter(
        student_id=student.id, sent_to_faculty_id=faculty.id
    )
    received_msgs = Faculty_Messages.objects.filter(
        faculty_id=faculty.id, sent_to_student_id=student.id
    )

    # Attach sender_type
    all_messages = []
    for msg in sent_msgs:
        d = model_to_dict(msg)
        d["sender_type"] = "student"
        Student = Students.objects.get(id=msg.student_id)
        name = Student.name
        d["name"] = name
        d["sent_at"] = msg.sent_at.strftime("%H:%M:%S %d %b %Y")
        all_messages.append(d)

    for msg in received_msgs:
        d = model_to_dict(msg)
        d["sender_type"] = "faculty"
        Faculty = Faculties.objects.get(id=msg.faculty_id)
        name = Faculty.name
        d["name"] = name
        d["sent_at"] = msg.sent_at.strftime("%H:%M:%S %d %b %Y")
        all_messages.append(d)

    # Sort by timestamp
    all_messages.sort(key=lambda x: x["sent_at"])

    return JsonResponse({"messages": all_messages})

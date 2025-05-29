from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from Home.models import Students, Faculties, sections

from .models import Faculty_Messages, Student_Messages
from django.utils import timezone
from datetime import datetime
from django.db.models import Q
from django.http import JsonResponse
from itertools import chain
from operator import attrgetter

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


@login_required
def message(request, user_id):
    current_user = request.user

    if request.method == "POST":
        content = request.POST.get("content")
        file = request.FILES.get("file")

        if not current_user.is_staff:
            faculty = get_object_or_404(Faculties, id=user_id)

            Student_Messages.objects.create(
                student_id=current_user.id,
                sent_to_faculty_id=faculty.id,
                content=content,
                file=file,
                sent_at=timezone.now(),
                status="sent"
            )

        else:
            student = get_object_or_404(Students, id=user_id)

            Faculty_Messages.objects.create(
                faculty_id=current_user.id,
                sent_to_student_id=student.id,
                content=content,
                file=file,
                sent_at=timezone.now(),
                status="sent"
            )

    return render(request, "message_form.html", {"user_id": user_id})


@login_required
def chatbox(request, user_id):
    current_user = request.user

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
            msg.sender_type = "You"
        for msg in received_msgs:
            msg.sender_type = "Other"

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
            msg.sender_type = "You"
        for msg in received_msgs:
            msg.sender_type = "Other"

    messages = sorted(chain(sent_msgs, received_msgs), key=attrgetter("sent_at"))

    context = {
        "messages": messages,
        "user_id": user_id,
        "currrent_user":request.user,
         
        # "user_id": other_user.id,
        "current_user_id": request.user.id,
}
    
    return render(request, "chatbox.html", context)


@login_required
def get_messages(request, user_id):
    current_user = request.user

    if not current_user.is_staff:
        student = current_user
        faculty = get_object_or_404(Faculties, id=user_id)

        # Mark unread faculty messages as read
        Faculty_Messages.objects.filter(
            faculty_id=faculty.id,
            sent_to_student_id=student.id,
            status="sent"
        ).update(status="read")

        sent_msgs = Student_Messages.objects.filter(
            student_id=student.id, sent_to_faculty_id=faculty.id
        )
        received_msgs = Faculty_Messages.objects.filter(
            faculty_id=faculty.id, sent_to_student_id=student.id
        )

    else:
        faculty = current_user
        student = get_object_or_404(Students, id=user_id)

        # Mark unread student messages as read
        Student_Messages.objects.filter(
            student_id=student.id,
            sent_to_faculty_id=faculty.id,
            status="sent"
        ).update(status="read")

        sent_msgs = Faculty_Messages.objects.filter(
            faculty_id=faculty.id, sent_to_student_id=student.id
        )
        received_msgs = Student_Messages.objects.filter(
            student_id=student.id, sent_to_faculty_id=faculty.id
        )

    all_messages = []

    for msg in sent_msgs:
        all_messages.append({
            "id": msg.id,
            "content": msg.content,
            "sent_at": msg.sent_at.strftime("%H:%M:%S %d %b %Y"),
            "file_url": msg.file.url if msg.file else None,
            "status": msg.status,
            "sender_type": "faculty" if current_user.is_staff else "student",
            "name": "You"  # Sent by current user
        })

    for msg in received_msgs:
        all_messages.append({
            "id": msg.id,
            "content": msg.content,
            "sent_at": msg.sent_at.strftime("%H:%M:%S %d %b %Y"),
            "file_url": msg.file.url if msg.file else None,
            "status": msg.status,
            "sender_type": "student" if current_user.is_staff else "faculty",
            "name": Faculties.objects.get(id=msg.faculty_id).name if not current_user.is_staff else Students.objects.get(id=msg.student_id).name,
        })

    all_messages.sort(
        key=lambda x: datetime.strptime(x["sent_at"], "%H:%M:%S %d %b %Y"), 
        reverse=True  # Newest first in the list
    )
    
    return JsonResponse({"messages": all_messages})
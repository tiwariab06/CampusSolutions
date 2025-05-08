from django.shortcuts import render, redirect, HttpResponse
from FacultyUploads.models import *
import os
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from Home.views import *
from Home.models import *
from .models import *


from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from datetime import date
from django.shortcuts import redirect
from django.urls import reverse


# Display Pyq's.
@login_required(login_url="/student/login/")
def showPyq(request):

    if request.method == "POST":
        sem = request.POST.get("semester")
        session = request.POST.get("session")
        item = Pyq.objects.filter(semester=sem, session=session)
        context = {
            "item": item,
        }
        return render(request, "showPyq.html", context)

    return render(request, "showPyq.html", {"isPyq": True})


# download Pyq's.


@login_required(login_url="/student/login/")
def downloadPyq(request, id):
    pyq = get_object_or_404(Pyq, id=id)
    file_path = pyq.url.path  # Get the file path as a string
    file_extension = os.path.splitext(file_path)[1]  # Extract the file extension
    response = HttpResponse(pyq.url, content_type="application/force-download")
    response["Content-Disposition"] = 'attachment; filename="%s%s"' % (
        pyq.name,
        file_extension,
    )
    return response


@login_required(login_url="/student/login/")
def showNotes(request):
    sub = subjects.objects.filter()
    if request.method == "POST":
        semester = request.POST.get("semester")
        subject = request.POST.get("subject")

        # fetching the notes from the database

        item = Notes.objects.filter(semester=semester, sub_name=subject)

        context = {
            "item": item,
            "isNotes": True,
            "subjects": sub,
        }
        return render(request, "showNotes.html", context)
    else:

        for i in sub:
            print(i.subject)
        context = {
            "isNotes": True,
            "subjects": sub,
        }
        return render(request, "showNotes.html", context)


@login_required(login_url="/student/login/")
def downloadNotes(request, id):
    pyq = get_object_or_404(Pyq, id=id)
    file_path = Notes.url.path  # Get the file path as a string
    file_extension = os.path.splitext(file_path)[1]  # Extract the file extension
    response = HttpResponse(pyq.url, content_type="application/force-download")
    response["Content-Disposition"] = 'attachment; filename="%s%s"' % (
        pyq.name,
        file_extension,
    )
    return response


@login_required(login_url="/student/login/")
def showAssignment(request):
    subs = subjects.objects.filter()
    assignments = []
    selected_subject = None

    if request.method == "POST":
        selected_subject = request.POST.get("subject")
        assignments = Assignments.objects.filter(
            subject=selected_subject, section=request.user.section
        )

    context = {
        "assignments": assignments,
        "subjects": subs,
        "selected_subject": selected_subject,
        "current_year": date.today().year,
    }
    return render(request, "showAssignment.html", context)


@login_required(login_url="/student/login/")
def downloadAssignment(request, id):
    assignment = get_object_or_404(Assignments, id=id)
    file_path = assignment.path.path
    file_extension = os.path.splitext(file_path)[1]
    response = HttpResponse(assignment.path, content_type="application/force-download")
    response["Content-Disposition"] = (
        f'attachment; filename="{assignment.subject}_Assignment_{assignment.assignment_number}{file_extension}"'
    )
    return response


@login_required()
def submitAssignment(request):
    if request.method == "POST":
        assignment_id = request.POST.get("assignment_id")
        assignment = Assignments.objects.get(id=assignment_id)
        Submitted_Assignments.objects.create(
            subject=assignment.subject,
            assignment_number=assignment.assignment_number,
            section=assignment.section,
            semester=assignment.semester,
            description=assignment.description,
            submission_deadline=assignment.submission_deadline,
            path=request.FILES["path"],
            submitted_on=timezone.now(),
        )
        return redirect(f"{reverse('showAssignment')}?submitted=true")


@login_required
def view_submitted_assignments(request):
    user = request.user
    sections = user.section.all()  # assuming m2m: faculty.sections
    selected_section = request.GET.get("section")

    submitted_assignments = Submitted_Assignments.objects.none()

    if selected_section:
        submitted_assignments = Submitted_Assignments.objects.filter(
            section=selected_section
        )

    context = {
        "sections": sections,
        "selected_section": selected_section,
        "submitted_assignments": submitted_assignments,
    }

    return render(request, "view_submitted_assignments.html", context)

from django.shortcuts import render, redirect, HttpResponse
from FacultyUploads.models import *
import os
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from Home.views import *
from Home.models import *
from .models import *
from .forms import *


from django.shortcuts import render, get_object_or_404
from django.http import FileResponse
from datetime import date
from django.shortcuts import redirect


# Create your views here.
@login_required
def choose_section_view(request):
    faculty = request.user
    sections = faculty.section.all()
    return render(request, "choose_section.html", {"sections": sections})


@login_required
def student_list_view(request, section_id):
    faculty = request.user
    section = get_object_or_404(faculty.section.all(), id=section_id)

    students = Students.objects.filter(section=section.section)

    return render(
        request, "students_list.html", {"students": students, "section": section}
    )


@login_required
def upload_result_view(request, student_id):
    student = get_object_or_404(Students, id=student_id)
    faculty = request.user
    subjects = faculty.subjects.filter()
    section = sections.objects.get(section=student.section)
    if request.method == "POST":
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.student = student
            result.save()
            messages.success(request, "Result uploaded successfully.")
            return redirect("upload_result", student.id)
    else:
        form = ResultForm()
        form.fields["subject"].choices = [(s.subject, s.subject) for s in subjects]

    return render(
        request,
        "upload_result.html",
        {"form": form, "student": student, "subjects": subjects},
    )



@login_required
def view_results(request):
    student = request.user # assuming OneToOne with User
    selected_exam = request.GET.get('exam_type', '')  # Get selected exam type from GET params

    exam_choices = ['Sessional 1', 'Sessional 2', 'Pre University Test (PUT)']

    if selected_exam:
        results = Result.objects.filter(student_id=student.id, Exam_Type=selected_exam)
    else:
        results = []

    context = {
        'exam_choices': exam_choices,
        'selected_exam': selected_exam,
        'results': results
    }

    return render(request, 'view_results.html', context)
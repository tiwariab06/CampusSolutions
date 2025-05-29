from django.shortcuts import render, redirect, HttpResponse
from .forms import *  # Import all forms
from .models import *  # Import all models
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.utils import DatabaseError
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from dateutil import parser


# Home Page View
def home(request):
    """
    Renders the home page.
    """
    return render(request, "home.html")


# Student Signup View
def studentsignup(request):
    """
    Handles student signup functionality:
    - POST: Validate and save the signup form data.
    - Redirect to the login page if successful, or display errors if invalid.
    - GET: Render an empty signup form.
    """
    if request.method == "POST":
        form = StudentSignup(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/login/student")
        else:
            errors = form.errors
            return render(request, "err.html", {"errors": errors})
    else:
        form = StudentSignup()
    return render(request, "studentsignup.html", {"form": form})


# Student Login View
@csrf_exempt
@never_cache
def studentlogin(request):
    """
    Handles student login functionality:
    - POST: Authenticate the user with the provided credentials.
      - If successful, log the user in and redirect to the student dashboard.
      - If failed, display an error message.
    - GET: Render the login page.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user and not user.is_staff:  # Verify user is not staff
            login(request, user)
            return render(request, "Dashboard.html")
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect("/login/student")
    else:
        return render(request, "login.html")


# Faculty Signup View
def facultysignup(request):
    """
    Handles faculty signup functionality:
    - POST: Validate and save the signup form, including many-to-many fields.
      - Redirect to the login page if successful.
      - Render an error page with form errors if invalid.
    - GET: Render an empty signup form.
    """
    if request.method == "POST":
        form = Facultysignup(request.POST)
        if form.is_valid():
            faculty = form.save(commit=False)
            faculty.save()
            form.save_m2m()
            messages.success(request, "Successfully Signed Up. Please Login.")
            return redirect("/login/faculty")
        else:
            errors = form.errors
            return render(request, "err.html", {"errors": errors})
    else:
        form = Facultysignup()
    return render(request, "facultysignup.html", {"form": form})


# Faculty Login View
@csrf_exempt
def facultylogin(request):
    """
    Handles faculty login functionality:
    - POST: Authenticate the user with the provided credentials.
      - If successful, log the user in and redirect to the home page.
      - If failed, display an error message.
    - GET: Render the login page.
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user and user.is_staff:  # Verify user is staff
            login(request, user)
            return render(request, "Dashboard.html")
        else:
            messages.error(request, "Invalid Username or Password")
            return redirect("/login/faculty")
    else:
        return render(request, "facultylogin.html")


# Logout View
@never_cache
@login_required(login_url="/")
def studentlogout(request):
    """
    Logs out the user and redirects to the home page.
    """
    logout(request)
    return redirect("/")


# Faculty Attendance Selection View
@never_cache
@login_required(login_url="/login/faculty/")
def select_section(request):
    """
    Allows faculty to select a section and subject for marking attendance.
    - Fetches and displays sections and subjects assigned to the logged-in faculty.
    """
    if request.user.is_authenticated:
        faculty = request.user
        assigned_sections = faculty.section.all()
        assigned_subjects = faculty.subjects.all()
        context = {
            "sections": assigned_sections,
            "subjects": assigned_subjects,
        }
        return render(request, "select_section.html", context)
    else:
        return render(request, "err.html", {"message": "Unauthorized access"})


# Fetch Students for Attendance View
@never_cache
@login_required(login_url="/login/faculty/")
def get_students(request):
    """
    Fetches a list of students based on the selected section and subject.
    - POST: Retrieves and renders the list of students for marking attendance.
    """
    if request.method == "POST":
        section_name = request.POST.get("section")
        subject_name = request.POST.get("subject")
        try:
            section = sections.objects.get(section=section_name)
            subject = subjects.objects.get(subject=subject_name)
            students = Students.objects.filter(section=section_name).values(
                "id", "name", "roll_number"
            )
            return render(
                request,
                "mark_attendance.html",
                {"students": students, "section": section, "subject": subject},
            )
        except sections.DoesNotExist:
            return render(
                request, "error.html", {"message": "Invalid section selected."}
            )
        except subjects.DoesNotExist:
            return render(
                request, "error.html", {"message": "Invalid subject selected."}
            )
    return render(request, "mark_attendance.html")


# Mark Attendance View
@never_cache
@login_required(login_url="/login/faculty/")
def mark_attendance(request):
    """
    Marks attendance for students based on the selected section and subject.
    - POST: Saves attendance data and redirects to the student list page.
    """
    if request.method == "POST":
        subject_name = request.POST.get("subject")
        section_name = request.POST.get("section")
        attendance_data = request.POST.getlist("attendance")

        try:
            subject = subjects.objects.get(subject=subject_name)
            section = sections.objects.get(section=section_name)
            students = Students.objects.filter(section=section_name)

            for student in students:
                status = "Present" if str(student.id) in attendance_data else "Absent"
                Attendance.objects.create(
                    student=student,
                    subject=subject,
                    section=section,
                    status=status,
                    date=timezone.now(),
                )

            messages.success(request, "Attendance marked successfully.")
            return redirect("get_students")
        except Exception as e:
            messages.error(request, "An error occurred while saving attendance.")
    return redirect("select_section")


# View Attendance for Students
@never_cache
@login_required(login_url="/")
def view_attendance(request):
    """
    Displays attendance details for the logged-in student.
    - Calculates attendance percentage and renders the attendance page.
    """
    try:
        student_id = request.user.id
        subject = subjects.objects.filter()
        # student=request.user
        # student_section = student.section
        # section_object = sections.objects.get(section=student_section)
        # sec_id = section_object.id
        # assigned_faculties = Faculties.objects.filter(section=sec_id)
        # assigned_faculties = Faculties.objects.filter()
        # print(assigned_faculties)
        print(len(subject))
        students_present = Attendance.objects.filter(
            status="Present", student_id=student_id
        )
        students_absent = Attendance.objects.filter(
            status="Absent", student_id=student_id
        )
        present = len(students_present)
        absent = len(students_absent)
        total = present + absent
        percentage = (present / total) * 100 if total > 0 else 0
        context = {
            "percentage": percentage,
            "subjects": subject,
        }
        return render(request, "Attendance.html", context)
    except DatabaseError:
        return render(
            request,
            "error.html",
            {"error_message": "Database error occurred. Please try again later."},
        )
    except ZeroDivisionError:
        return render(
            request,
            "Attendance.html",
            {"percentage": 0, "error_message": "No attendance records available."},
        )
    except Exception as e:
        return render(
            request,
            "error.html",
            {"error_message": "An unexpected error occurred. Please contact support."},
        )


@login_required
def subject_wise_attendance(request):
    try:
        if request.method == "POST":
            student_id = request.user.id
            subject_id = request.POST.get("subject")
            subject_name_ob = subjects.objects.get(id=subject_id)
            subject_name = subject_name_ob.subject
            all_subject = subjects.objects.filter()
            print(subject_id)

            # get records
            present = Attendance.objects.filter(
                status="Present", student_id=student_id, subject_id=subject_id
            )
            absent = Attendance.objects.filter(
                status="Absent", student_id=student_id, subject_id=subject_id
            )

            times_present = len(present)
            times_absent = len(absent)

            total = times_present + times_absent
            percentage_subject = (times_present / total) * 100 if total > 0 else 0
            context = {
                "percentage_subject": percentage_subject,
                "subject_name": subject_name,
                "subjects": all_subject,
            }
            return render(request, "Attendance.html", context)
    except DatabaseError:
        return render(
            request,
            "error.html",
            {"error_message": "Database error occurred. Please try again later."},
        )
    except ZeroDivisionError:
        return render(
            request,
            "Attendance.html",
            {"percentage": 0, "error_message": "No attendance records available."},
        )
    except Exception as e:
        return render(
            request,
            "error.html",
            {"error_message": "An unexpected error occurred. Please contact support."},
        )


@login_required
def filter_attendance_by_date(request):
    """
    Filters attendance records for the logged-in student based on a selected date or date range.
    """
    if request.method == "POST":
        start_date = request.POST.get("start_date")  # Retrieve start date from the form
        end_date = request.POST.get("end_date")  # Retrieve end date from the form
        student_id = request.user.id  # Get the logged-in user's ID
        print(student_id)

        if start_date and end_date:  # If both dates are provided
            attendances_total = Attendance.objects.filter(
                student_id=student_id,  # Filter by logged-in student
                # Filter by date range
            )
            attendances = attendances_total.filter(date__range=[start_date, end_date])
            present = Attendance.objects.filter(
                status="Present",
                student_id=student_id,
            )  # Present records for the student
            absent = Attendance.objects.filter(
                status="Absent",
                student_id=student_id,
            )  # Absent records for the student

            total = present.count() + absent.count()
            print(absent.count())
            percentage_date = (present.count() / total) * 100 if total > 0 else 0

            return render(
                request,
                "date_attendance.html",
                {
                    "attendances": attendances,
                    "start_date": start_date,
                    "end_date": end_date,
                    "percentage_date": percentage_date,
                },
            )
        elif start_date:  # If only the start date is provided
            attendances = Attendance.objects.filter(
                student_id=student_id,  # Filter by logged-in student
                date=start_date,  # Filter by the exact start date
            )

            return render(
                request,
                "date_attendance.html",
                {
                    "attendances": attendances,
                    "start_date": start_date,
                },
            )
        else:
            attendances = Attendance.objects.none()  # No valid date input
            return render(request, "date_attendance.html", {"attendances": attendances})

    # GET request - render the form template
    return render(request, "Attendance.html", {"attendances": None})


from datetime import timedelta, date


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.contrib import messages
from django.utils.timezone import now
from datetime import datetime
from .models import Attendance, Students, subjects, sections  # adjust import as needed


@never_cache
@login_required(login_url="/login/faculty/")
def edit_attendance(request):
    if request.method == "POST":
        section_id = request.POST.get("section")
        subject_id = request.POST.get("subject")
        date_str = request.POST.get("date")
        print(date_str)

        try:
            sec = sections.objects.get(id=section_id)
            subject = subjects.objects.get(id=subject_id)
        except (sections.DoesNotExist, subjects.DoesNotExist):
            return render(
                request, "error.html", {"message": "Invalid section or subject."}
            )

        faculty = request.user
        if sec not in faculty.section.all() or subject not in faculty.subjects.all():
            return render(
                request,
                "error.html",
                {"message": "Unauthorized access to section or subject."},
            )

        if not date_str:
            return render(request, "error.html", {"message": "Please select a date."})

        try:
            selected_date = parser.parse(date_str).date()
        except (ValueError, TypeError):
            return render(
                request,
                "error.html",
                {
                    "message": f"Invalid date format: '{date_str}'. Please enter a valid date."
                },
            )

        if (now().date() - selected_date).days > 3:
            return render(
                request,
                "error.html",
                {"message": "Editing allowed only within 3 days of marking."},
            )

        if "save_changes" in request.POST:
            for student_id in request.POST.getlist("student_ids"):
                try:
                    student = Students.objects.get(id=student_id)
                    attendance = Attendance.objects.get(
                        student_id=student,
                        section_id=sec,
                        subject_id=subject,
                        date=selected_date,
                    )
                    status = (
                        "Present"
                        if f"attendance_{student_id}" in request.POST
                        else "Absent"
                    )
                    attendance.status = status
                    attendance.save()
                except Attendance.DoesNotExist:
                    continue
            messages.success(request, "Attendance updated successfully.")
            return redirect(
                "edit_attendance"
            )  # Update to the correct name of your URL pattern

        attendance_records = Attendance.objects.filter(
            section_id=sec, subject_id=subject, date=selected_date
        ).select_related("student")

        return render(
            request,
            "edit_attendance.html",
            {
                "attendance_records": attendance_records,
                "section": sec,
                "subject": subject,
                "date": selected_date,
            },
        )

    # GET request: Show section and subject selection form
    faculty = request.user
    assigned_sections = faculty.section.all()
    assigned_subjects = faculty.subjects.all()
    return render(
        request,
        "choose_edit_attendance.html",
        {
            "sections": assigned_sections,
            "subjects": assigned_subjects,
        },
    )


def profile(request):
    return render(request, "profile.html")

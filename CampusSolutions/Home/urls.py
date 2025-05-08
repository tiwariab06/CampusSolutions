"""
URL configuration for CampusSolutions project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views
from Home.forms import CustomPasswordResetForm

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.studentsignup, name="studentsignup"),
    path("login/", views.studentlogin, name="studentlogin"),
    path("login/dashboard/", views.studentlogin, name="studentlogindash"),
    path("logout/", views.studentlogout, name="logout"),
    path("signup/faculty/", views.facultysignup, name="facultysignup"),
    path("login/faculty/", views.facultylogin, name="facultylogin"),
    path("mark_attendance/", views.mark_attendance, name="mark_attendance"),
    path("login/faculty/select_section/", views.select_section, name="select_section"),
    path("login/faculty/get_students/", views.get_students, name="get_students"),
    path("view_attendance/", views.view_attendance, name="view_attendace"),
    path(
        "attendance/subject",
        views.subject_wise_attendance,
        name="subject_wise_attendance",
    ),
    path(
        "attendance/date",
        views.filter_attendance_by_date,
        name="filter_attendance_by_date",
    ),
    path("attendance/edit/", views.edit_attendance, name="edit_attendance"),

    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="password_reset.html", form_class=CustomPasswordResetForm
        ),
        name="password_reset",
    ),

    path("reset_password_done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]

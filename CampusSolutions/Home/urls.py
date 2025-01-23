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
]

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("show/Pyq/", views.showPyq, name="showPyq"),
    path("show/Notes/", views.showNotes, name="showNotes"),
    path("download/Pyq/<int:id>/", views.downloadPyq, name="downloadPyq"),
    path("download/Notes/<int:id>/", views.downloadNotes, name="downloadNotes"),
    path("show/assignments/", views.showAssignment, name="showAssignment"),
    path(
        "download/assignments/<int:id>/",
        views.downloadAssignment,
        name="downloadAssignment",
    ),
    path("submit-assignment/", views.submitAssignment, name="submitAssignment"),
    path(
        "submissions/",
        views.view_submitted_assignments,
        name="view_submitted_assignments",
    ),
]

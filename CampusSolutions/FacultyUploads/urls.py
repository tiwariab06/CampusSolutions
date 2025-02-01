from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("upload/Pyq/", views.UploadPyq, name="UploadPyq"),
    path("upload/Notes", views.uploadNotes, name="uploadNotes"),
    path("upload/Assignments", views.uploadAssignmnets, name="uploadAssignments"),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )  # for working of file uploads correctly

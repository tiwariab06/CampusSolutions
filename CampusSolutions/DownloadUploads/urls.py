from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("show/Pyq/", views.showPyq, name="showPyq"),
    path("download/Pyq/<int:id>/", views.downloadPyq, name="downloadPyq"),
]

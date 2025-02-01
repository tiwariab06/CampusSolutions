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


# Upload Pyqs


@login_required(login_url="/login/faculty/")
def UploadPyq(request):
    if request.method == "POST":
        form = PyqForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Pyq uploaded successfully!")
            return redirect("/upload/Pyq")  # Replace with the actual URL name
        else:
            messages.error(request, "Please enter correct data.")
    else:
        form = PyqForm()

    return render(request, "uploadPyq.html", {"form": form})


# view for uploading Notes


@login_required(login_url="/login/faculty/")
def uploadNotes(request):
    if request.method == "POST":
        form = notesForm(request.POST, request.FILES)
        if form.is_valid():
            print("reached here")
            form.save()
            messages.success(request, "Notes uploaded successfully!")
            return redirect("/upload/Notes")  # Replace with the actual URL name
        else:
            messages.error(request, "Please enter correct data.")
    else:
        form = notesForm()

    return render(request, "uploadData.html", {"form": form})


# view for uploading Assignments


@login_required(login_url="/login.faculty")
def uploadAssignmnets(request):
    if request.method == "POST":

        form = assignmentForm(request.POST, request.FILES, request=request)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment Uploaded Sucessfully")
            return redirect("/upload/Assignments")
        else:
            messages.error(request, "Please reverify the Data")
    else:
        form = assignmentForm(request=request)
    return render(request, "uploadData.html", {"form": form})

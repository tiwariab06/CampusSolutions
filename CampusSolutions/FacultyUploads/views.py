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

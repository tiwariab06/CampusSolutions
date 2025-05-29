from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from datetime import date
from .models import Students, Attendance


# views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import RegisteredFace

# from MainApp.models import Student  # Assuming your original Student model is in MainApp
import face_recognition
import numpy as np
import os


@login_required
def register_face_view(request):
    user = request.user
    print(user.id)
    # Check if face already registered
    if RegisteredFace.objects.filter(user=user).exists():
        return render(request, "error.html", {"msg": "Face already registered."})

    # Get student profile
    try:
        student = Students.objects.get(id=user.id)
    except Students.DoesNotExist:
        return render(request, "error.html", {"msg": "Student profile not found."})

    if request.method == "POST" and request.FILES.get("face_image"):
        face_image = request.FILES["face_image"]

        # Save temporarily for encoding
        temp_path = f"temp_faces/{student.roll_number}.jpg"
        os.makedirs(os.path.dirname(temp_path), exist_ok=True)

        with open(temp_path, "wb+") as f:
            for chunk in face_image.chunks():
                f.write(chunk)

        # Process encoding
        img = face_recognition.load_image_file(temp_path)
        encodings = face_recognition.face_encodings(img)

        if encodings:
            npy_path = f"face_encodings/{student.roll_number}.npy"
            os.makedirs("face_encodings", exist_ok=True)
            np.save(npy_path, encodings[0])

            # Save RegisteredFace instance
            RegisteredFace.objects.create(
                user=user,
                student_id=student.id,
                name=student.name,
                roll_number=student.roll_number,
                email=user.email,
                face_image=face_image,
            )
            os.remove(temp_path)
            return render(
                request,
                "student_face_register.html",
                {"msg": "Face registered successfully"},
            )
        else:
            os.remove(temp_path)
            return render(
                request,
                "error.html",
                {"msg": "No face detected. Try again with a clearer image."},
            )

    return render(request, "student_face_register.html")


# AutoAttendance/views.py
from django.shortcuts import render, redirect
from .forms import AttendanceScanForm
from .scanner import run_face_attendance  # <-- we will create this
from django.contrib import messages


def scan_attendance_view(request):
    if request.method == "POST":
        form = AttendanceScanForm(request.POST, request=request)
        if form.is_valid():
            section = form.cleaned_data["section"]
            subject = form.cleaned_data["subject"]

            result = run_face_attendance(subject.id, section.id)

            messages.success(
                request,
                f"Attendance scan completed. {result['marked']} marked, {result['skipped']} skipped.",
            )
            return redirect("attendance_scan")  # or any result page
    else:
        form = AttendanceScanForm(request=request)

        return render(request, "attendance_scan.html", {"form": form})

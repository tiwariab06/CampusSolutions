from django.urls import path
from .views import register_face_view, scan_attendance_view

urlpatterns = [
    # path("api/mark_attendance/", mark_attendance),
    path("register-face/", register_face_view, name="register_face"),
    path("scan/", scan_attendance_view, name="attendance_scan"),
]

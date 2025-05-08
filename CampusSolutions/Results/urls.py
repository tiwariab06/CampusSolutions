from django.urls import path
from . import views

urlpatterns = [
    path("upload-results/", views.choose_section_view, name="choose_section"),
    path(
        "upload-results/section/<int:section_id>/",
        views.student_list_view,
        name="student_list",
    ),
    path(
        "upload-results/student/<int:student_id>/",
        views.upload_result_view,
        name="upload_result",
    ),
    path("results/", views.view_results, name="view_results"),
]

# urls.py

from django.urls import path
from .views import upload_resource, show_resources

urlpatterns = [
    path('resources/upload/', upload_resource, name='upload_resource'),
    path('resources/', show_resources, name='show_resources'),
]

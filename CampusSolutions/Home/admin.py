from django.contrib import admin
from .models import Students, sections, subjects, Faculties, Attendance

admin.site.register(Students)
admin.site.register(sections)
admin.site.register(subjects)
admin.site.register(Faculties)
admin.site.register(Attendance)

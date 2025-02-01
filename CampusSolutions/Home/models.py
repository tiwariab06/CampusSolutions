from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class sections(models.Model):
    id = models.AutoField(primary_key=True)
    section = models.CharField(max_length=100)

    def __str__(self):
        return self.section


class subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.subject


class Students(AbstractUser):
    id = models.AutoField(
        primary_key=True
    )  # ✅ Fix 1: Ensures integer primary key instead of ObjectId
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    roll_number = models.CharField(max_length=50, unique=True)
    year = models.IntegerField()
    branch = models.CharField(max_length=100)
    section = models.CharField(max_length=20)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="student_users",
        blank=True,
        help_text="The groups this student belongs to.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="student_user_permissions",
        blank=True,
        help_text="Specific permissions for this student.",
    )

    def __str__(self):
        return self.username


class Faculties(AbstractUser):
    id = models.AutoField(
        primary_key=True
    )  # ✅ Fix 1: Ensures integer primary key instead of ObjectId

    YEAR_CHOICES = [
        ("1", "First Year"),
        ("2", "Second Year"),
        ("3", "Third Year"),
        ("4", "Fourth Year"),
    ]

    DEPARTMENT_CHOICES = [
        ("CSE", "Computer Science and Engineering"),
        ("ECE", "Electronics and Communication Engineering"),
        ("ME", "Mechanical Engineering"),
        ("CE", "Civil Engineering"),
    ]

    name = models.CharField(max_length=100)
    department = models.CharField(max_length=200, choices=DEPARTMENT_CHOICES)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)

    section = models.ManyToManyField(
        "sections"
    )  # ✅ Fix 2: Used string reference for ManyToManyField
    subjects = models.ManyToManyField(
        "subjects"
    )  # ✅ Fix 2: Used string reference for ManyToManyField

    is_staff = models.BooleanField(default=True)

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="faculty_users",
        blank=True,
        help_text="The groups this faculty belongs to.",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="faculty_user_permissions",
        blank=True,
        help_text="Specific permissions for this faculty.",
    )


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)

    student = models.ForeignKey(
        "Students", on_delete=models.CASCADE, related_name="attendances"
    )  # ✅ Fix 3: Used string reference for ForeignKey
    subject = models.ForeignKey(
        "subjects", on_delete=models.CASCADE
    )  # ✅ Fix 3: Used string reference
    section = models.ForeignKey(
        "sections", on_delete=models.CASCADE
    )  # ✅ Fix 3: Used string reference

    status = models.CharField(max_length=50)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.student.username} - {self.subject.subject} - {self.date} - {self.status}"

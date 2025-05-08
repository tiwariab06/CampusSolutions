from django import forms
from .models import *
from Home.models import subjects

class assignmentForm(forms.ModelForm):
    semester = forms.ChoiceField(
        choices=Submitted_Assignments.Semester.choices,
        label="Semester",
        widget=forms.Select(attrs={"class": "col-md-6"}),
    )

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)  # Extract request from kwargs
        super().__init__(*args, **kwargs)

        if request and request.user.is_authenticated:
            # Ensure the user is authenticated before using their info
            print("hi")
            user = request.user
            assigned_sections = user.section.all()  # Sections assigned to the user
            assigned_subjects = user.subjects.all()  # Subjects assigned to the user
            print("ho")
            self.fields["section"] = forms.ModelChoiceField(
                queryset=assigned_sections,
                widget=forms.Select(attrs={"class": "col-md-6"}),
                empty_label="Select Section",  # Optional, to provide a placeholder
            )

            self.fields["subject"] = forms.ModelChoiceField(
                queryset=assigned_subjects,
                widget=forms.Select(attrs={"class": "col-md-6"}),
                empty_label="Select Subject",  # Optional, to provide a placeholder
            )

    class Meta:
        model = Assignments
        fields = [
            "subject",
            "assignment_number",
            "path",
            "department",
            "semester",
            "section",
            "description",
            "submission_deadline",
        ]
        widgets = {
            "assignment_number": forms.NumberInput(
                attrs={"class": "col-md-6", "placeholder": "Enter number b/w 1-5 only"}
            ),
            "description": forms.TextInput(attrs={"class": "col-md-6"}),
            "submission_deadline": forms.DateInput(
                attrs={"class": "col-md-6", "type": "date"}
            ),
            "department": forms.Select(attrs={"class": "col-md-6"}),
        }
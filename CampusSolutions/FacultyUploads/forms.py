from django import forms
from .models import *
from Home.models import subjects


class PyqForm(forms.ModelForm):

    semester = forms.ChoiceField(
        choices=Pyq.Semester.choices,
        label="Semester",
        widget=forms.Select(attrs={"class": "col-md-6"}),
    )

    class Meta:
        model = Pyq
        fields = ["url", "name", "semester", "session"]

        widgets = {
            "session": forms.TextInput(attrs={"placeholder": "Use 20XX-20XX Format"})
        }

    def save(self, commit=True):
        # Save the instance but do not immediately commit to the database
        instance = super().save(commit=False)
        if commit:
            instance.save()  # Save to the database if commit is True
        return instance


class notesForm(forms.ModelForm):
    semester = forms.ChoiceField(
        choices=Notes.Semester.choices,
        label="Semester",
        widget=forms.Select(attrs={"class": "col-md-6"}),
    )
    sub_name=forms.ModelChoiceField(queryset=subjects.objects.filter())
    class Meta:
        model = Notes
        fields = ["path", "sub_name", "semester", "type"]

        widgets = {
            "type": forms.Select(attrs={"class": "col-md-6  "}),
            "sub_name": forms.TextInput(attrs={"class": "col-md-6  "}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance


# form for Assignments Upload


from django import forms
from .models import Assignments


class assignmentForm(forms.ModelForm):
    semester = forms.ChoiceField(
        choices=Assignments.Semester.choices,
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

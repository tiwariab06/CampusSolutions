from django import forms
from .models import *


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

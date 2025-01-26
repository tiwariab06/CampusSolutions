from django import forms
from .models import Pyq

class PyqForm(forms.ModelForm):
    class Meta:
        model = Pyq
        fields = ["url", "name", "semester", "session"]

    def save(self, commit=True):
        # Save the instance but do not immediately commit to the database
        instance = super().save(commit=False)
        if commit:
            instance.save()  # Save to the database if commit is True
        return instance

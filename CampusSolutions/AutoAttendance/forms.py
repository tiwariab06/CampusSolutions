from django import forms
from Home.models import subjects, sections

class AttendanceScanForm(forms.Form):
    section = forms.ModelChoiceField(queryset=sections.objects.none())
    subject = forms.ModelChoiceField(queryset=subjects.objects.none())

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        user = request.user if request else None

        if user:
            self.fields['section'].queryset = user.section.all()
            self.fields['subject'].queryset = user.subjects.all()

        # Add Bootstrap classes to widgets
        self.fields['section'].widget.attrs.update({
            'class': 'form-select',
            'style': 'border-radius: 8px; padding: 8px;'
        })
        self.fields['subject'].widget.attrs.update({
            'class': 'form-select',
            'style': 'border-radius: 8px; padding: 8px;'
        })

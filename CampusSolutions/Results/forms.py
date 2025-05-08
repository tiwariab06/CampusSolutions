from django import forms
from .models import Result

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['Exam_Type', 'subject', 'max_marks', 'obtained_marks']
        widgets = {
            'Exam_Type': forms.Select(attrs={'class': 'form-select form-label'}),
            'subject': forms.Select(attrs={'class': 'form-select form-label'}),
            'max_marks': forms.NumberInput(attrs={'class': 'form-control form-label'}),
            'obtained_marks': forms.NumberInput(attrs={'class': 'form-control form-label'}),
        }

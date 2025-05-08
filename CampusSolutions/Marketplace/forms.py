# forms.py

from django import forms
from .models import Resources

class ResourceForm(forms.ModelForm):
    TYPE_CHOICES = [
        ('Notes', 'Notes'),
        ('Book', 'Book'),
        ('Guide', 'Guide'),
    ]
    PRINT_CHOICES = [
        ('Printed', 'Printed'),
        ('Handwritten', 'Handwritten'),
    ]

    Type = forms.ChoiceField(choices=TYPE_CHOICES)
    Print = forms.ChoiceField(choices=PRINT_CHOICES)

    class Meta:
        model = Resources
        fields = '__all__'

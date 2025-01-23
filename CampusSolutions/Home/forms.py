from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password

class StudentSignup(forms.ModelForm):
    section = forms.ModelChoiceField(
        queryset=sections.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select your section'
        }),
        required=True
    )
    class Meta:
        model=Students
        fields=['name','email','username','password','roll_number','year','branch','section']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),
             'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
             'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password'
            }),
             'roll_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your Roll'
            }),
             'year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your year'
            }),
             'branch': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your branch'
            }),
             
        }

    def save(self, commit=True):
         instance = super().save(commit=False)
         instance.password = make_password(self.cleaned_data['password'])  # Hash the password
         if commit:
            instance.save()
         return instance


class Facultysignup(forms.ModelForm):
   

    subjects = forms.ModelMultipleChoiceField(
        queryset=subjects.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'placeholder': 'Select subjects'
        })
    )

    class Meta:
        model = Faculties
        fields = ['username', 'email','password', 'name', 'year', 'department', 'section', 'subjects']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your password'
            }),
            'year': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your year'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select your department'
            }),
            'section': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'placeholder': 'Select your Sections'
            }),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.password = make_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            instance.save()
        return instance
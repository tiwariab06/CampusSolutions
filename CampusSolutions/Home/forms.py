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

    semester = forms.ChoiceField(
        choices=[(i, f"Semester {i}") for i in range(1, 9)],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select your semester'
        }),
        required=True
    )

    branch = forms.ChoiceField(
        choices=[
            ('CSE', 'Computer Science'),
            ('ECE', 'Electronics and Communication'),
            ('ME', 'Mechanical Engineering'),
            ('CE', 'Civil Engineering'),
            ('EE', 'Electrical Engineering'),
            # Add more branches if needed
        ],
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Select your branch'
        }),
        required=True
    )

    class Meta:
        model = Students
        fields = ['name', 'email', 'username', 'password', 'roll_number', 'semester', 'branch', 'section']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your username'
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
                'placeholder': 'Enter your Roll Number'
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


from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth import get_user_model


class CustomPasswordResetForm(PasswordResetForm):
   def get_users(self, email):
    UserModel = get_user_model()
    try:
        # Use filter instead of raw query
        users = UserModel.objects.filter(email=email, is_active=True)
        return list(users) if users else []
    except Exception as e:
        # Handle exception (e.g., log it)
        return []



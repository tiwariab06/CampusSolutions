# your_project/Home/authentication/authentication_backend.py
from django.contrib.auth.backends import BaseBackend
from ..models import Faculties

class FacultyAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            # Retrieve the faculty by username (email or username)
            user = Faculties.objects.get(username=username)
            
            # Check the password by comparing the raw password with the hashed one
            if user.check_password(password):  # check_password handles hashing and comparison
                return user  # If passwords match, return the user
        except Faculties.DoesNotExist:
            return None  # Return None if no matching faculty is found
    
    def get_user(self,id_):
        try:
            return Faculties.objects.get(pk=id_) # <-- tried to get by email here
        except Faculties.DoesNotExist:
            return None

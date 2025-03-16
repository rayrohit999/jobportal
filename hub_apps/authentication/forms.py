from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    is_recruiter = forms.BooleanField(required=False, label="Register as Recruiter")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'profile_picture', 'password1', 'password2', 'is_recruiter']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
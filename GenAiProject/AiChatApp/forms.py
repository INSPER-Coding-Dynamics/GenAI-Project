from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_superuser = False
        user.is_staff = False
        if commit:
            user.save()
        return user
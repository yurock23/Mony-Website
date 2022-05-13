
"""
Celeste Ha, Linh Luu, Yurock Heo
COM214 Final Project
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):

	class Meta(UserCreationForm):
		model = CustomUser
		fields = ('first_name','last_name','username', 'address', 'email',)


class CustomUserChangeForm(UserChangeForm):

	class Meta:
		model = CustomUser
		fields = ('first_name','last_name','username', 'address', 'email',)
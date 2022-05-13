"""
Celeste Ha, Linh Luu, Yurock Heo
COM214 Final Project
"""
from django.urls import path
from .views import SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
]
"""
Celeste Ha, Linh Luu, Yurock Heo
COM214 Final Project
"""
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
	address = models.CharField(max_length=100, blank=True, null=True)
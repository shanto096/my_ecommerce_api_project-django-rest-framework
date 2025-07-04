# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # অতিরিক্ত কাস্টম ফিল্ড যোগ করুন
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True) # ইউনিক রাখা ভালো
    address = models.TextField(blank=True, null=True)

    # এই মেথডটি ডিবাগিং-এর জন্য সহায়ক
    def __str__(self):
        return self.username
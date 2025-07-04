# accounts/urls.py
from django.urls import path, include

urlpatterns = [
    # Djoser এর ইউজার সম্পর্কিত এন্ডপয়েন্ট: /users/, /users/me/, /users/set_password/ ইত্যাদি
    path('', include('djoser.urls')),
    # টোকেন-ভিত্তিক লগইন ও লগআউট: /token/login/, /token/logout/
    path('', include('djoser.urls.authtoken')),
    # JWT ব্যবহার করতে চাইলে: path('', include('djoser.urls.jwt')),
]
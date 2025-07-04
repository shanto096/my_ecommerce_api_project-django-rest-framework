# accounts/serializers.py
from djoser.serializers import UserCreateSerializer as DjoserUserCreateSerializer, UserSerializer as DjoserUserSerializer
from rest_framework import serializers
from .models import User

class UserCreateSerializer(DjoserUserCreateSerializer):
    class Meta(DjoserUserCreateSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'password', 'phone_number', 'address')
        extra_kwargs = {'password': {'write_only': True}} # পাসওয়ার্ড শুধুমাত্র রাইটের জন্য

class UserSerializer(DjoserUserSerializer):
    class Meta(DjoserUserSerializer.Meta):
        model = User
        fields = ('id', 'username', 'email', 'phone_number', 'address', 'first_name', 'last_name') # প্রয়োজনে আরও ফিল্ড যোগ করুন
        read_only_fields = ('email',) # ইমেইল রিড-অনলি করা যেতে পারে
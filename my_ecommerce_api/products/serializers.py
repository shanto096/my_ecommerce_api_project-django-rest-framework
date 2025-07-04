# products/serializers.py
from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True) # যখন প্রোডাক্ট গেট করা হবে, তখন ক্যাটাগরির পুরো ডিটেইলস দেখাবে
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False, allow_null=True
    ) # প্রোডাক্ট তৈরি বা আপডেটের সময় ক্যাটাগরির ID পাঠানোর জন্য

    class Meta:
        model = Product
        fields = '__all__' # সব ফিল্ড ইনক্লুড করা হয়েছে
        # read_only_fields = ('created_at', 'updated_at') # এগুলো অটো জেনারেট হয়
# cart/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer # প্রোডাক্ট ডিটেইলস দেখানোর জন্য
from products.models import Product # <--- এই লাইনটি যোগ করুন!

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) # প্রোডাক্টের পুরো তথ্য দেখাবে
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), # <--- এখানে Product ব্যবহার করা হচ্ছে
        source='product',
        write_only=True
    ) # কার্টে প্রোডাক্ট যোগ করার সময় প্রোডাক্ট ID পাঠানোর জন্য

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']
        read_only_fields = ['total_price'] # এটি একটি @property

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True) # কার্টের আইটেমগুলো দেখাবে
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True) # কার্টের মোট মূল্য

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']
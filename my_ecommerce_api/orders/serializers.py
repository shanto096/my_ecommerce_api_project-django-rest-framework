# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer # প্রোডাক্টের ডিটেইলস দেখানোর জন্য
from products.models import Product # <--- এই লাইনটি যোগ করুন!

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True) # প্রোডাক্টের পুরো তথ্য দেখাবে
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), # <--- এখানে Product মডেল ব্যবহার করতে হবে, ProductSerializer নয়।
        source='product',
        write_only=True
    )

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price', 'total_price']
        read_only_fields = ['total_price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_amount', 'status', 'payment_status',
                  'shipping_address', 'transaction_id', 'created_at', 'updated_at']
        read_only_fields = ['user', 'total_amount', 'status', 'payment_status', 'transaction_id',
                            'created_at', 'updated_at']
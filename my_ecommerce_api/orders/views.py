# orders/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from django.db import transaction # অ্যাটোমিক অপারেশনের জন্য
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderItemSerializer
from cart.models import Cart, CartItem
from products.models import Product

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # শুধুমাত্র ব্যবহারকারীর অর্ডারগুলো দেখাবে
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        # সরাসরি অর্ডার তৈরি করা (যদি কার্ট ব্যবহার না করে হয়) - এই ক্ষেত্রে আইটেম ম্যানুয়ালি পাঠাতে হবে
        # এটি জটিল, তাই কার্ট থেকে অর্ডার তৈরি করার পদ্ধতিই বেশি ব্যবহৃত হয়।
        # এখানে আমরা শুধু ডামি সেভ করছি।
        serializer.save(user=self.request.user, status='pending', payment_status='pending')


    @action(detail=False, methods=['post'])
    def create_order_from_cart(self, request):
        """
        ব্যবহারকারীর কার্ট থেকে একটি অর্ডার তৈরি করে।
        স্টক আপডেট করে এবং কার্ট খালি করে।
        """
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"detail": "Cart not found for this user."}, status=status.HTTP_404_NOT_FOUND)

        cart_items = cart.items.all()
        if not cart_items:
            return Response({"detail": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        shipping_address = request.data.get('shipping_address')
        if not shipping_address:
            return Response({"detail": "Shipping address is required to create an order."}, status=status.HTTP_400_BAD_REQUEST)


        with transaction.atomic(): # নিশ্চিত করুন যে সম্পূর্ণ অপারেশন সফল বা ব্যর্থ হয়
            order = Order.objects.create(
                user=request.user,
                shipping_address=shipping_address,
                status='pending',
                payment_status='pending',
                total_amount=0 # প্রাথমিক মান, পরে আপডেট হবে
            )

            total_order_amount = 0
            order_items_to_create = []
            for cart_item in cart_items:
                product = cart_item.product
                quantity = cart_item.quantity

                if product.stock < quantity:
                    # স্টক পর্যাপ্ত না হলে ট্রানজেকশন রোলব্যাক হবে
                    raise serializers.ValidationError(
                        f"Not enough stock for {product.name}. Available: {product.stock}, Requested: {quantity}"
                    )

                # পণ্যের স্টক আপডেট করুন
                product.stock -= quantity
                product.save()

                # অর্ডার আইটেম তৈরি করুন
                order_item = OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.price # অর্ডারের সময় পণ্যের বর্তমান মূল্য সেভ করা হয়
                )
                order_items_to_create.append(order_item)
                total_order_amount += order_item.total_price

            OrderItem.objects.bulk_create(order_items_to_create)

            # অর্ডারের মোট মূল্য আপডেট করুন
            order.total_amount = total_order_amount
            order.save()

            # কার্ট খালি করুন (বা কার্ট আইটেমগুলো ডিলিট করুন)
            cart_items.delete()

            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def mark_as_paid(self, request, pk=None):
        """
        একটি অর্ডারের পেমেন্ট স্ট্যাটাস 'paid' এ আপডেট করে।
        """
        order = self.get_object()
        if order.payment_status == 'pending':
            order.payment_status = 'paid'
            # এখানে আপনি আপনার পেমেন্ট গেটওয়ের ট্রানজেকশন আইডি সেভ করতে পারেন
            order.transaction_id = request.data.get('transaction_id', None)
            order.save()
            serializer = self.get_serializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail": "Order is already paid or cannot be marked as paid."}, status=status.HTTP_400_BAD_REQUEST)
# cart/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Cart, CartItem
from products.models import Product
from .serializers import CartSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated] # শুধুমাত্র লগইন করা ব্যবহারকারী তাদের কার্ট অ্যাক্সেস করতে পারবে

    def get_queryset(self):
        # শুধুমাত্র লগইন করা ব্যবহারকারীর কার্ট দেখাবে
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # একটি নতুন কার্ট তৈরি করার সময়, যদি ইউজারের কার্ট না থাকে
        # এটি সাধারণত `get_or_create` দিয়ে পরিচালনা করা হয়, যা নিচে `my_cart` অ্যাকশনে করা হয়েছে
        # কিন্তু যদি আপনি সরাসরি Cart তৈরি করতে চান, তাহলে ensure user has no existing cart
        if not Cart.objects.filter(user=self.request.user).exists():
            serializer.save(user=self.request.user)
        else:
            raise serializers.ValidationError("User already has a cart.")


    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        # ব্যবহারকারীর কার্ট ফিরিয়ে দেয়, যদি না থাকে তবে তৈরি করে
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # শুধুমাত্র ব্যবহারকারীর কার্টের আইটেম দেখাবে
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        # কার্ট আইটেম তৈরি করার সময়, ব্যবহারকারীর কার্ট খুঁজে বের করুন বা তৈরি করুন
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']

        # প্রোডাক্টের স্টক চেক করুন
        if product.stock < quantity:
            return Response(
                {"detail": f"Not enough stock for {product.name}. Available: {product.stock}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # যদি আইটেমটি ইতিমধ্যেই কার্টে থাকে, তাহলে পরিমাণ আপডেট করুন
        existing_item = CartItem.objects.filter(cart=cart, product=product).first()
        if existing_item:
            if (existing_item.quantity + quantity) > product.stock:
                return Response(
                    {"detail": f"Adding {quantity} to cart would exceed stock. Current: {existing_item.quantity}, Available: {product.stock}"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            existing_item.quantity += quantity
            existing_item.save()
            serializer = self.get_serializer(existing_item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer.save(cart=cart) # নতুন আইটেম যোগ করুন
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        product = serializer.instance.product
        new_quantity = serializer.validated_data.get('quantity', serializer.instance.quantity)

        if new_quantity > product.stock:
             return Response(
                {"detail": f"Cannot set quantity to {new_quantity}. Available: {product.stock}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()
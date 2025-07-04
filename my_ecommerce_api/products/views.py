# products/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # অথেন্টিকেটেড হলে রিড/রাইট, নাহলে শুধু রিড

    def get_permissions(self):
        # এডমিন ইউজাররা ক্যাটাগরি ক্রিয়েট, আপডেট, ডিলিট করতে পারবে
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly] # অন্যান্য অ্যাকশনের জন্য
        return [permission() for permission in self.permission_classes]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        # এডমিন ইউজাররা প্রোডাক্ট ক্রিয়েট, আপডেট, ডিলিট করতে পারবে
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAdminUser]
        else:
            self.permission_classes = [IsAuthenticatedOrReadOnly]
        return [permission() for permission in self.permission_classes]
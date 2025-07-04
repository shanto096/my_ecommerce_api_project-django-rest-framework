# orders/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('orders/create-from-cart/', OrderViewSet.as_view({'post': 'create_order_from_cart'}), name='create-order-from-cart'),
    # যদি mark_as_paid একটি নির্দিষ্ট অর্ডার ID এর সাথে কাজ করে
    path('orders/<int:pk>/mark-as-paid/', OrderViewSet.as_view({'post': 'mark_as_paid'}), name='order-mark-as-paid'),
]
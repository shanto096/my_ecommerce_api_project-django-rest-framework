# orders/models.py
from django.db import models
from django.conf import settings
from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping_address = models.TextField()
    payment_status = models.CharField(max_length=20, default='pending') # 'pending', 'paid', 'failed'
    transaction_id = models.CharField(max_length=100, blank=True, null=True) # পেমেন্ট গেটওয়ে থেকে প্রাপ্ত ID

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def save(self, *args, **kwargs):
        # অর্ডার সেভ করার আগে যদি total_amount ০ থাকে তাহলে গণনা করুন
        if not self.id and self.total_amount == 0: # নতুন অর্ডার এবং total_amount সেট করা হয়নি
            super().save(*args, **kwargs) # প্রথমে অর্ডার সেভ করুন যাতে ID পাওয়া যায়
            self.total_amount = sum(item.total_price for item in self.items.all())
            super().save(update_fields=['total_amount'])
        else:
            super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2) # অর্ডার তৈরির সময় পণ্যের দাম

    class Meta:
        unique_together = ('order', 'product') # একটি অর্ডারে একই প্রোডাক্ট একাধিকবার যোগ হওয়া এড়াতে

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for Order {self.order.id}"

    @property
    def total_price(self):
        return self.quantity * self.price
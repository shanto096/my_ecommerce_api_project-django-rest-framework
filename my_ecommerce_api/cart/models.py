# cart/models.py
from django.db import models
from django.conf import settings # User মডেল অ্যাক্সেস করার জন্য
from products.models import Product # Product মডেল অ্যাক্সেস করার জন্য

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_price(self):
        # কার্টের মোট মূল্য গণনা
        return sum(item.total_price for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product') # একটি কার্টে একই প্রোডাক্ট একাধিকবার যোগ হওয়া এড়াতে

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart.user.username}'s cart"

    @property
    def total_price(self):
        return self.quantity * self.product.price
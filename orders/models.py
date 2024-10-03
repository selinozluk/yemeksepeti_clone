from django.db import models
from users.models import User  # Kullanıcı modelini kullanmak için import
from restaurants.models import MenuItem  # MenuItem modelini doğru yerden import


# Sipariş Modeli
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order {self.id} by {self.user.email}'


# Sipariş Öğesi Modeli
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product_name} x {self.quantity}'


# Sepet Modeli
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart for {self.user.email}'


# Sepet Öğesi Modeli
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(MenuItem, on_delete=models.CASCADE)  # MenuItem ile bağlantı
    quantity = models.PositiveIntegerField(null=False)  # null=False ekleniyor
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Fiyat doğrudan MenuItem'dan alınmalı
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.product.name} x {self.quantity} - {self.product.price * self.quantity} total'

   # Sepet öğesi kaydedildiğinde ürün fiyatını güncelle
def save(self, *args, **kwargs):
    if self.product.price is None:
        raise ValueError("Ürün fiyatı tanımlı değil.")  # Ürün fiyatı tanımsızsa hata verir
    self.price = self.product.price * self.quantity  # Fiyatı, ürünün fiyatı ile çarp
    super().save(*args, **kwargs)

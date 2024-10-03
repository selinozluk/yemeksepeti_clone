from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at', 'updated_at')  # Alan isimleri düzeltildi
    list_filter = ('created_at', 'updated_at')  # Alan isimleri düzeltildi
    search_fields = ('user__email',)
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product_name', 'quantity', 'price', 'created_at', 'updated_at')  # Alan isimleri düzeltildi
    list_filter = ('created_at', 'updated_at')  # Alan isimleri düzeltildi
    search_fields = ('product_name',)  # Alan ismi düzeltildi


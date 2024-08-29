# restaurants/admin.py

from django.contrib import admin
from .models import Restaurant, MenuItem, Category

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone', 'createdAt', 'updatedAt')
    list_filter = ('createdAt', 'updatedAt')
    search_fields = ('name', 'address')
    inlines = [MenuItemInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # 'restaurant' alanı kaldırıldı
    search_fields = ('name',)  # 'list_filter' kaldırıldı çünkü restaurant alanı artık yok

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'category', 'name', 'price', 'createdAt', 'updatedAt')
    list_filter = ('createdAt', 'updatedAt', 'category', 'restaurant')
    search_fields = ('name', 'description')

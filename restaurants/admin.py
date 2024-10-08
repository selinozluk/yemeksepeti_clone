# restaurants/admin.py

from django.contrib import admin
from .models import Restaurant, MenuItem, RestaurantCategory, MenuItemCategory

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'address')
    inlines = [MenuItemInline]

@admin.register(RestaurantCategory)
class RestaurantCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # 'restaurant' alanı kaldırıldı
    search_fields = ('name',)  # 'list_filter' kaldırıldı çünkü restaurant alanı artık yok

@admin.register(MenuItemCategory)
class MenuItemCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'category', 'name', 'price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'category', 'restaurant')
    search_fields = ('name', 'description')
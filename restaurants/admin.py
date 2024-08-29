from django.contrib import admin
from .models import Restaurant, MenuItem, Category  # Category modelini de import ettik

class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone', 'createdAt', 'updatedAt')
    list_filter = ('createdAt', 'updatedAt')
    search_fields = ('name', 'address')
    inlines = [MenuItemInline]  # Restaurant admini için inline olarak MenuItem ekledik

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'restaurant')
    list_filter = ('restaurant',)
    search_fields = ('name',)

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'restaurant', 'category', 'name', 'price', 'createdAt', 'updatedAt')
    list_filter = ('createdAt', 'updatedAt', 'category')
    search_fields = ('name', 'description')

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'firstName', 'lastName', 'isAdmin', 'is_staff', 'is_active', 'is_customer')
    list_filter = ('isAdmin', 'is_staff', 'is_active', 'is_customer')
    
    def has_view_permission(self, request, obj=None):
        return request.user.is_staff or request.user.isAdmin

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff or request.user.isAdmin

    def has_delete_permission(self, request, obj=None):
        return request.user.is_staff or request.user.isAdmin

    def has_add_permission(self, request):
        return request.user.is_staff or request.user.isAdmin
    
    # created_at ve updated_at alanlarını yalnızca okunabilir yapıyoruz
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),  # Temel alanlar
        ('Personal Info', {'fields': ('firstName', 'lastName', 'birthDate')}),  # Kişisel bilgiler
        ('Permissions', {'fields': ('isAdmin', 'is_staff', 'is_active', 'is_customer')}),  # Yetkiler
        ('Important dates', {'fields': ('last_login', 'created_at', 'updated_at')}),  # Tarih alanları
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'firstName', 'lastName', 'birthDate', 'isAdmin', 'is_staff', 'is_active', 'is_customer')},
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)


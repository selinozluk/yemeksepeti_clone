from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'firstName', 'lastName', 'isAdmin', 'is_staff', 'is_active')
    list_filter = ('isAdmin', 'is_staff', 'is_active')
    
    # createdAt ve updatedAt alanlarını yalnızca okunabilir yapıyoruz
    readonly_fields = ('createdAt', 'updatedAt')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('firstName', 'lastName', 'birthDate')}),
        ('Permissions', {'fields': ('isAdmin', 'is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'createdAt', 'updatedAt')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'firstName', 'lastName', 'birthDate', 'isAdmin', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)

from django.urls import path
from .views import user_login, register, password_reset  # login yerine user_login import edildi

urlpatterns = [
    path('login/', user_login, name='login'),  # user_login olarak güncellendi
    path('register/', register, name='register'),
    path('password-reset/', password_reset, name='password_reset'),  # Şifre sıfırlama URL'i
]

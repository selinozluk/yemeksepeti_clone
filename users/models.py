from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email alanı doldurulmalıdır.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Parola burada hash'leniyor ve saklanıyor
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('isAdmin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('isAdmin') is not True:
            raise ValueError('Süper kullanıcı isAdmin=True olmalıdır.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Süper kullanıcı is_staff=True olmalıdır.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Süper kullanıcı is_superuser=True olmalıdır.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    firstName = models.CharField(max_length=255, verbose_name="İsim")
    lastName = models.CharField(max_length=255, verbose_name="Soyisim")
    email = models.EmailField(unique=True, verbose_name="Email")
    birthDate = models.DateField(null=True, blank=True, verbose_name="Doğum Tarihi")
    isAdmin = models.BooleanField(default=False, verbose_name="Yönetici mi?")
    is_staff = models.BooleanField(default=False, verbose_name="Personel mi?")
    is_active = models.BooleanField(default=True, verbose_name="Aktif mi?")
    createdAt = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updatedAt = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName']

    def __str__(self):
        return self.email

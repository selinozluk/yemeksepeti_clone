from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=255, label='Ad')
    last_name = forms.CharField(max_length=255, label='Soyad')
    phone_number = forms.CharField(max_length=15, label='Telefon Numarası')
    birth_date = forms.DateField(
        label='Doğum Tarihi', 
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'gg.aa.yyyy'})
    )
    email = forms.EmailField(label='Email')

    password1 = forms.CharField(
        label='Şifre',
        widget=forms.PasswordInput,
        help_text="Şifre aşağıdakileri içermelidir:\n"
                  "- En az 10 karakter\n"
                  "- En az bir büyük harf (A-Z)\n"
                  "- En az bir küçük harf (a-z)\n"
                  "- En az bir rakam (0-9)\n"
                  "- En az bir özel karakter (!@#$%^&*()-_=+)"
    )

    password2 = forms.CharField(
        label='Şifre Tekrarı',
        widget=forms.PasswordInput,
        help_text='Doğrulama için şifreyi tekrar girin.'
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'birth_date', 'email', 'phone_number', 'password1', 'password2']

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 10:
            raise forms.ValidationError('Şifre en az 10 karakter olmalıdır.')
        if not any(char.isupper() for char in password):
            raise forms.ValidationError('Şifre en az bir büyük harf içermelidir (A-Z).')
        if not any(char.islower() for char in password):
            raise forms.ValidationError('Şifre en az bir küçük harf içermelidir (a-z).')
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('Şifre en az bir rakam içermelidir (0-9).')
        if not any(char in '!@#$%^&*()-_=+' for char in password):
            raise forms.ValidationError('Şifre en az bir özel karakter içermelidir (!@#$%^&*()-_=+).')
        return password

# Şifre sıfırlama formu dışarıda tanımlandı
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Email")
    phone_number = forms.CharField(max_length=15, label="Telefon Numarası")

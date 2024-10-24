from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login  # Django'nun login fonksiyonu
from django.http import HttpResponseRedirect
from .models import User
from .forms import UserRegistrationForm
from .forms import PasswordResetForm
from django.core.mail import send_mail
from cryptography.fernet import Fernet
from django.conf import settings

# Fernet şifreleme anahtarı
cipher_suite = Fernet(settings.FERNET_KEY)

def user_login(request):  # Bu fonksiyonu 'user_login' olarak adlandırdık
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect('/')
        else:
            return render(request, 'users/login.html', {'error': 'Hatalı email veya şifre.'})
    else:
        return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.firstName = form.cleaned_data['first_name']
            user.lastName = form.cleaned_data['last_name']
            user.birthDate = form.cleaned_data['birth_date']
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password1'])
            user.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect('/')
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def password_reset(request):
    if request.method == 'POST':
        print("POST verileri:", request.POST)  # POST verilerini terminale yazdır
        form = PasswordResetForm(request.POST)
        
        if form.is_valid():
            contact_method = form.cleaned_data.get('contact_method')  # Kullanıcının seçtiği yöntem (e-posta veya telefon)
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            print("Email:", email)
            print("Phone:", phone_number)

            # Kullanıcı e-posta ile sıfırlama seçtiyse
            if contact_method == 'email':
                user = User.objects.filter(email=email).first()
                if user:
                    # Eğer telefon numarası da doldurulmuşsa ve uyuşmuyorsa hata ekle
                    if phone_number and user.phone_number != phone_number:
                        form.add_error('phone_number', 'Girdiğiniz telefon numarası bu e-posta adresiyle uyuşmuyor.')
                    else:
                        # Doğrulama başarılı, e-posta için token oluştur ve gönder
                        token = cipher_suite.encrypt(user.email.encode())
                        print("Oluşturulan E-posta Token:", token.decode())  # Token'ı yazdır
                        send_mail(
                            'Şifre Sıfırlama Talebi',
                            f'Sıfırlama için bu linki kullanın: {request.build_absolute_uri()}?token={token.decode()}',
                            'no-reply@yemeksepeti_clone.com',
                            [user.email],
                        )
                        return render(request, 'users/password_reset_done.html', {'message': 'E-posta adresinize bir sıfırlama kodu gönderildi.'})
                else:
                    form.add_error('email', 'Bu e-posta adresi ile kayıtlı bir kullanıcı bulunamadı.')

            # Kullanıcı telefon numarası ile sıfırlama seçtiyse
            elif contact_method == 'phone':
                user = User.objects.filter(phone_number=phone_number).first()
                if user:
                    # Eğer e-posta adresi de doldurulmuşsa ve uyuşmuyorsa hata ekle
                    if email and user.email != email:
                        form.add_error('email', 'Girdiğiniz e-posta adresi bu telefon numarasıyla uyuşmuyor.')
                    else:
                        # Doğrulama başarılı, telefon için token oluştur
                        token = cipher_suite.encrypt(user.phone_number.encode())
                        print("Oluşturulan Telefon Token:", token.decode())  # Token'ı yazdır
                        return render(request, 'users/password_reset_done.html', {'message': f'Telefon numaranıza bir sıfırlama kodu gönderildi: {token.decode()}'})
                else:
                    form.add_error('phone_number', 'Bu telefon numarası ile kayıtlı bir kullanıcı bulunamadı.')

        # Form geçerli değilse form hatalarını yazdır
        print("Form Hataları:", form.errors)
    else:
        form = PasswordResetForm()

    return render(request, 'users/password_reset.html', {'form': form})

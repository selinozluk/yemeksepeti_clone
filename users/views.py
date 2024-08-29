from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponseRedirect
from .models import User  # Kendi User modelinizi import edin
from .forms import UserRegistrationForm  # Kullanıcı kayıt formunu import edin

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)  # Authentication için email kullanılıyor
        if user is not None:
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Backend belirtildi
            return HttpResponseRedirect('/')  # Başarılı girişten sonra yönlendirilecek URL
        else:
            # Hatalı giriş
            return render(request, 'users/login.html', {'error': 'Hatalı email veya şifre.'})
    else:
        # GET isteği
        return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Formdan alınan verileri kullanıcı modeline ekleyin
            user.firstName = form.cleaned_data['first_name']
            user.lastName = form.cleaned_data['last_name']
            user.birthDate = form.cleaned_data['birth_date']
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password1'])  # Şifreyi set_password ile ayarlayın
            user.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')  # Backend belirtildi
            return HttpResponseRedirect('/')  # Başarılı kayıt sonrası yönlendirilecek URL
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


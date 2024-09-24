from pathlib import Path
import os
import environ

# environ kurulumu
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2#35v7l9p&bohq8=@cv7h!ne0_-4vn@ldycij)rw8tw56$=%@n'
JWT_ALGORITHM = "HS256"  # Bu satır düzeltildi

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Elastic IP adresi ve localhost gibi IP'ler ALLOWED_HOSTS'e eklendi
ALLOWED_HOSTS = ['35.169.62.192', '10.0.0.25', 'localhost', '127.0.0.1']  

# AWS S3 ayarları
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'yemeksepeti-clone-media'
AWS_S3_REGION_NAME = 'us-east-1'  # Bucket bölgesi
AWS_S3_FILE_OVERWRITE = False  # Aynı dosya ismiyle yüklendiğinde üzerine yazılmasın
AWS_DEFAULT_ACL = None  # Herkesin dosyalara erişim izni olmasın
AWS_QUERYSTRING_AUTH = False  # İsteğe bağlı, URL'de imza olmadan dosya erişimi sağlar
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'  # Varsayılan depolama S3 olarak ayarlanıyor

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',  # Users uygulaması eklendi
    'orders', # Orders eklendi
    'restaurants', # Restoranlar eklendi
    'graphene_django',  # Graphene-Django eklendi
    'django_filters',  # Django-Filter eklendi
    'corsheaders',  # CORS Headers eklendi
    'graphql_jwt',  # JWT Authentication eklendi
    'storages',  # Django storages eklendi
    'yemeksepeti_clone',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS Middleware eklendi
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'yemeksepeti_clone.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'yemeksepeti_clone.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yemeksepeti-clone',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# Custom user model
AUTH_USER_MODEL = 'users.User'  # Kullanıcı modelini değiştirmek için eklenen satır


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Media URL S3 ile bağlantısı
MEDIA_URL = 'https://yemeksepeti-clone-media.s3.amazonaws.com/Proje%20Yemekleri/'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# GraphQL Ayarları
GRAPHENE = {
    "SCHEMA": "yemeksepeti_clone.schema.schema",  # Schema dosyasının yolu
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
        "graphene_django.debug.DjangoDebugMiddleware",
    ],
}

# JWT Ayarları
AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# CORS Ayarları
CORS_ALLOW_ALL_ORIGINS = True  # Geliştirme sırasında tüm alan adlarına izin verilebilir

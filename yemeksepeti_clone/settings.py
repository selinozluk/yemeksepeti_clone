from pathlib import Path
import os
import pymysql

# PyMySQL kullanımı için eklenen satır
pymysql.install_as_MySQLdb()

# Proje dizinini tanımlama
BASE_DIR = Path(__file__).resolve().parent.parent

# Güvenlik anahtarı, ortam değişkeni olarak ayarlandı
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'django-insecure-2#35v7l9p&bohq8=@cv7h!ne0_-4vn@ldycij)rw8tw56$=%@n')

# DEBUG modu, ortam değişkenine bağlı olarak ayarlandı
DEBUG = os.getenv('DJANGO_DEBUG', 'False') == 'True'

# İzin verilen hostlar, ortam değişkenine bağlı olarak ayarlandı
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', 'localhost 127.0.0.1').split()

# Uygulama tanımları
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',  # Users uygulaması eklendi
    'orders',  # Orders eklendi
    'restaurants',  # Restoranlar eklendi
    'graphene_django',  # Graphene-Django eklendi
    'django_filters',  # Django-Filter eklendi
    'corsheaders',  # CORS Headers eklendi
    'graphql_jwt',  # JWT Authentication eklendi
]

# Middleware tanımları
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

# URL yapılandırma
ROOT_URLCONF = 'yemeksepeti_clone.urls'

# Şablon ayarları
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

# WSGI uygulaması
WSGI_APPLICATION = 'yemeksepeti_clone.wsgi.application'

# Veritabanı ayarları
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'yemeksepeti-clone'),
        'USER': os.getenv('MYSQL_USER', 'root'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'password'),
        'HOST': os.getenv('MYSQL_HOST', 'localhost'),
        'PORT': os.getenv('MYSQL_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# Özel kullanıcı modeli
AUTH_USER_MODEL = 'users.User'

# Şifre doğrulama ayarları
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

# Uluslararasılaştırma ayarları
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Statik dosyalar ayarları
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Medya dosyaları ayarları
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Varsayılan birincil anahtar alan tipi
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# GraphQL ayarları
GRAPHENE = {
    "SCHEMA": "yemeksepeti_clone.schema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
        "graphene_django.debug.DjangoDebugMiddleware",
    ],
}

# JWT doğrulama ayarları
AUTHENTICATION_BACKENDS = [
    'graphql_jwt.backends.JSONWebTokenBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# CORS ayarları
CORS_ALLOW_ALL_ORIGINS = True

# Güvenlik ayarları (üretim ortamı için)
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False') == 'True'
X_FRAME_OPTIONS = 'DENY'

# Logging ayarları
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

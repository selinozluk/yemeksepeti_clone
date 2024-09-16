import os
from django.core.wsgi import get_wsgi_application

# Django ayarlarının hangi dosyada olduğu
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yemeksepeti_clone.settings')

# WSGI sunucusunun çalışması için gerekli fonksiyonu 
application = get_wsgi_application()

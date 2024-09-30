import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from functools import wraps

User = get_user_model()

def roles_required(*roles):
    def wrapper(func):
        @wraps(func)
        def wrapped(root, info, *args, **kwargs):
            user = info.context.user
            if not user.is_authenticated:
                raise Exception("Giriş yapmadınız.")
            
            # Admin yetkisi kontrolü
            if "ADMIN" in roles and not user.is_superuser:
                raise Exception("Yetkiniz yok.")
            
            # Staff yetkisi kontrolü
            if "STAFF" in roles and not user.is_staff:
                print(f"Kullanıcı: {user.email}, Staff mı?: {user.is_staff}, Admin mi?: {user.is_superuser}")
                raise Exception("Yetkiniz yok.")


            return func(root, info, *args, **kwargs)
        return wrapped
    return wrapper

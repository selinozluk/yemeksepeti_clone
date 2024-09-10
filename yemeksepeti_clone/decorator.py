import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()

def roles_required(*roles):
    def wrapper(func):
        def wrapped(root,info,*args,**kwargs):
            # if "authorization" not in info.context["request"].headers:
            #     raise Exception("NOT AUTHORİZED")
            # context =  info.context["request"].headers
            # token = context.split(" ")[-1]
            # secret, algorithm = settings.SECRET_KEY, settings.JWT_ALGORITHM
            # payload = jwt.decode(token, secret, algorithm)
            # if "email" not in payload:
            #     raise Exception("NOT AUTHORİZED")
            # try:
            #     user =User.objects.get(email=payload["email"])
            # except User.DoesNotExist:
            #     raise Exception("USER NOT FOUND")
            # info.context.user = user
            user = info.context.user
            if "ADMIN" in roles and user.isAdmin:
                func(*args,**kwargsr)
            if "STAFF" in roles and user.is_staff:
                func(*args,**kwargsr)
            
        return wrapped
    return wrapper
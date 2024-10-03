from graphql_jwt.decorators import user_passes_test

def roles_required(*roles):
    def check_permission(user):
        # Admin her şeye erişebilir
        if user.isAdmin: 
            return True
        
        # Restoran sahibi ise kendi restoranına ait verilere erişebilir
        if "RESTAURANT_OWNER" in roles and user.is_restaurant_owner:
            return True

        # Müşteri kendi siparişlerine erişebilir
        if "CUSTOMER" in roles and user.is_customer:
            return True
        
        return False  # Yukarıdaki rollere sahip değilse erişim verilmez
    return user_passes_test(check_permission)

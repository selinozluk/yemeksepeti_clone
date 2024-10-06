import graphene
from graphene_django import DjangoObjectType
from orders.models import Order, OrderItem, Cart, CartItem
from restaurants.models import MenuItem
from yemeksepeti_clone.decorator import roles_required
from decimal import Decimal



# Sipariş modelini GraphQL için tanımlama
class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "user", "total_price", "created_at", "updated_at", "items")

# Sipariş öğesi modelini GraphQL için tanımlama
class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = ("id", "order", "product_name", "quantity", "price", "created_at", "updated_at")

# Sepet modeli için GraphQL tanımı
class CartType(DjangoObjectType):
    class Meta:
        model = Cart
        fields = ("id", "user", "items", "created_at", "updated_at")

# Sepet öğesi modeli için GraphQL tanımı
class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem
        fields = ("id", "cart", "product", "quantity", "price", "created_at", "updated_at")

# Sorgular
class Query(graphene.ObjectType):
    # Kullanıcının sadece kendi siparişlerini görmesi için
    all_orders = graphene.List(OrderType)
    
    @roles_required("CUSTOMER")
    def resolve_all_orders(root, info):
        user = info.context.user
        if user.is_authenticated:
            return Order.objects.filter(user=user)
        raise Exception("Giriş yapmalısınız.")

    # Belirli bir siparişi ID ile getirme
    order = graphene.Field(OrderType, id=graphene.Int(required=True))

    @roles_required("CUSTOMER", "STAFF")
    def resolve_order(root, info, id):
        user = info.context.user
        if user.is_authenticated:
            try:
                return Order.objects.get(pk=id, user=user)
            except Order.DoesNotExist:
                raise Exception("Sipariş bulunamadı.")
        raise Exception("Giriş yapmalısınız.")

    # Kullanıcının sepetini getirme
    user_cart = graphene.Field(CartType)

    @roles_required("CUSTOMER")
    def resolve_user_cart(self, info):
        user = info.context.user
        if user.is_authenticated:
            try:
                return Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                raise Exception("Sepet bulunamadı.")
        raise Exception("Giriş yapmalısınız.")

# Sipariş oluşturma mutasyonu
class CreateOrder(graphene.Mutation):
    class Arguments:
        total_price = graphene.Float(required=True) 

    order = graphene.Field(OrderType)

    @roles_required("CUSTOMER")
    def mutate(self, info, total_price):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Giriş yapmalısınız.")
        if total_price <= 0:
            raise Exception("Geçersiz toplam fiyat.")
        order = Order.objects.create(user=user, total_price=Decimal(total_price))  # total_price olarak düzeltildi
        return CreateOrder(order=order)



# Sipariş güncelleme mutasyonu
class UpdateOrder(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        total_price = graphene.Float()

    order = graphene.Field(OrderType)

    @roles_required("CUSTOMER", "STAFF")
    def mutate(self, info, id, total_price=None):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Giriş yapmalısınız.")
        try:
            order = Order.objects.get(pk=id, user=user)
        except Order.DoesNotExist:
            raise Exception("Sipariş bulunamadı.")
        
        if total_price is not None and total_price > 0:
            order.total_price = total_price
        
        order.save()
        return UpdateOrder(order=order)


# Sipariş silme mutasyonu
class DeleteOrder(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @roles_required("CUSTOMER", "STAFF")
    def mutate(self, info, id):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Giriş yapmalısınız.")
        try:
            order = Order.objects.get(pk=id, user=user)
            order.delete()
            return DeleteOrder(success=True)
        except Order.DoesNotExist:
            raise Exception("Sipariş bulunamadı.")



# Sipariş öğesi güncelleme mutasyonu
class UpdateOrderItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        product_name = graphene.String()
        quantity = graphene.Int()
        price = graphene.Float()

    order_item = graphene.Field(OrderItemType)

    @roles_required("CUSTOMER", "STAFF")
    def mutate(self, info, id, product_name=None, quantity=None, price=None):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Giriş yapmalısınız.")
        try:
            order_item = OrderItem.objects.get(pk=id, order__user=user)
        except OrderItem.DoesNotExist:
            raise Exception("Sipariş öğesi bulunamadı.")
        
        if product_name:
            order_item.product_name = product_name
        if quantity is not None and quantity > 0:
            order_item.quantity = quantity
        if price is not None and price > 0:
            order_item.price = price
        
        order_item.save()
        return UpdateOrderItem(order_item=order_item)

# Sipariş öğesi silme mutasyonu
class DeleteOrderItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @roles_required("CUSTOMER", "STAFF")
    def mutate(self, info, id):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Giriş yapmalısınız.")
        try:
            order_item = OrderItem.objects.get(pk=id, order__user=user)
            order_item.delete()
            return DeleteOrderItem(success=True)
        except OrderItem.DoesNotExist:
            raise Exception("Sipariş öğesi bulunamadı.")

# Sipariş öğesi oluşturma mutasyonu
class CreateOrderItem(graphene.Mutation):
    class Arguments:
        order_id = graphene.ID(required=True)
        product_id = graphene.ID(required=True)  # Ürün ID'sini aldık
        quantity = graphene.Int(required=True)

    order_item = graphene.Field(OrderItemType)

    @roles_required("CUSTOMER", "STAFF")
    def mutate(self, info, order_id, product_id, quantity):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Giriş yapmalısınız.")
        try:
            order = Order.objects.get(pk=order_id, user=user)
        except Order.DoesNotExist:
            raise Exception("Sipariş bulunamadı.")

        try:
            product = MenuItem.objects.get(pk=product_id)  # Ürünü bulduk
        except MenuItem.DoesNotExist:
            raise Exception("Ürün bulunamadı.")

        if quantity <= 0:
            raise Exception("Geçersiz ürün bilgileri.")

        # Ürün fiyatını otomatik olarak MenuItem'dan al
        order_item = OrderItem.objects.create(order=order, product_name=product.name, quantity=quantity, price=product.price)
        return CreateOrderItem(order_item=order_item)



# Sepet öğesi güncelleme mutasyonu
class UpdateCartItem(graphene.Mutation):
    class Arguments:
        cart_item_id = graphene.ID(required=True)
        quantity = graphene.Int(required=True)

    cart_item = graphene.Field(CartItemType)

    @roles_required("CUSTOMER")
    def mutate(self, info, cart_item_id, quantity):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Giriş yapmalısınız.")
        try:
            cart_item = CartItem.objects.get(pk=cart_item_id, cart__user=user)
            cart_item.quantity = quantity
            cart_item.save()
            return UpdateCartItem(cart_item=cart_item)
        except CartItem.DoesNotExist:
            raise Exception("Sepet öğesi bulunamadı.")

# Sepet öğesi silme mutasyonu
class DeleteCartItem(graphene.Mutation):
    class Arguments:
        cart_item_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @roles_required("CUSTOMER")
    def mutate(self, info, cart_item_id):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Giriş yapmalısınız.")
        try:
            cart_item = CartItem.objects.get(pk=cart_item_id, cart__user=user)
            cart_item.delete()
            return DeleteCartItem(success=True)
        except CartItem.DoesNotExist:
            raise Exception("Sepet öğesi bulunamadı.")

# Sepete öğe ekleme mutasyonu
class AddCartItem(graphene.Mutation):
    class Arguments:
        product_id = graphene.ID(required=True)
        quantity = graphene.Int(required=True)

    cart_item = graphene.Field(CartItemType)

    @roles_required("CUSTOMER")
    def mutate(self, info, product_id, quantity):
        user = info.context.user
        if not user.is_authenticated:
            raise Exception("Giriş yapmalısınız.")
        cart, created = Cart.objects.get_or_create(user=user)
        product = MenuItem.objects.get(id=product_id)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={"quantity":quantity})
        
        if not item_created:
            cart_item.quantity += quantity

        # Ürün fiyatını hesapla ve kaydet
        cart_item.price = product.price * cart_item.quantity  
        cart_item.save()
        
        return AddCartItem(cart_item=cart_item)

    

# Mutation sınıfı
class Mutation(graphene.ObjectType):
    # Sipariş işlemleri
    create_order = CreateOrder.Field()
    update_order = UpdateOrder.Field()
    delete_order = DeleteOrder.Field()
    
    # Sipariş öğesi işlemleri
    create_order_item = CreateOrderItem.Field()
    update_order_item = UpdateOrderItem.Field()
    delete_order_item = DeleteOrderItem.Field()
    
    # Sepet işlemleri
    add_cart_item = AddCartItem.Field()
    update_cart_item = UpdateCartItem.Field()
    delete_cart_item = DeleteCartItem.Field()

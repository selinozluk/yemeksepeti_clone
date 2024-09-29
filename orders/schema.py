import graphene
from graphene_django import DjangoObjectType
from orders.models import Order, OrderItem, Cart, CartItem
from users.models import User

# Sipariş modelini GraphQL için tanımlama
class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "user", "totalPrice", "createdAt", "updatedAt", "items")

# Sipariş öğesi modelini GraphQL için tanımlama
class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = ("id", "order", "productName", "quantity", "price", "createdAt", "updatedAt")

# Sepet modeli için GraphQL tanımı
class CartType(DjangoObjectType):
    class Meta:
        model = Cart
        fields = ("id", "user", "items", "createdAt", "updatedAt")

# Sepet öğesi modeli için GraphQL tanımı
class CartItemType(DjangoObjectType):
    class Meta:
        model = CartItem
        fields = ("id", "cart", "productName", "quantity", "price", "createdAt", "updatedAt")

# Sorgular
class Query(graphene.ObjectType):
    # Tüm siparişleri listeleme
    all_orders = graphene.List(OrderType)
    # Belirli bir siparişi ID ile getirme
    order = graphene.Field(OrderType, id=graphene.Int(required=True))
    
    # Belirli bir kullanıcının sepetini getirme
    user_cart = graphene.Field(CartType, user_id=graphene.ID(required=True))

    # Tüm siparişleri döndürme
    def resolve_all_orders(root, info):
        return Order.objects.all()

    # Belirli bir siparişi ID ile döndürme
    def resolve_order(root, info, id):
        try:
            return Order.objects.get(pk=id)
        except Order.DoesNotExist:
            raise Exception("Sipariş bulunamadı.")

    # Kullanıcının sepetini döndürme
    def resolve_user_cart(self, info, user_id):
        try:
            return Cart.objects.get(user_id=user_id)
        except Cart.DoesNotExist:
            raise Exception("Sepet bulunamadı.")

# Sipariş oluşturma mutasyonu
class CreateOrder(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        total_price = graphene.Float(required=True)

    order = graphene.Field(OrderType)

    def mutate(self, info, user_id, total_price):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Exception("Kullanıcı bulunamadı.")
        if total_price <= 0:
            raise Exception("Geçersiz toplam fiyat.")
        order = Order.objects.create(user=user, totalPrice=total_price)
        return CreateOrder(order=order)

# Sipariş güncelleme mutasyonu
class UpdateOrder(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        total_price = graphene.Float()

    order = graphene.Field(OrderType)

    def mutate(self, info, id, total_price=None):
        try:
            order = Order.objects.get(pk=id)
        except Order.DoesNotExist:
            raise Exception("Sipariş bulunamadı.")
        if total_price is not None and total_price > 0:
            order.totalPrice = total_price
        order.save()
        return UpdateOrder(order=order)

# Sipariş silme mutasyonu
class DeleteOrder(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            order = Order.objects.get(pk=id)
            order.delete()
            return DeleteOrder(success=True)
        except Order.DoesNotExist:
            raise Exception("Sipariş bulunamadı.")
        
# Sipariş öğesi oluşturma mutasyonu
class CreateOrderItem(graphene.Mutation):
    class Arguments:
        order_id = graphene.ID(required=True)
        product_name = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        price = graphene.Float(required=True)

    order_item = graphene.Field(OrderItemType)

    def mutate(self, info, order_id, product_name, quantity, price):
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            raise Exception("Sipariş bulunamadı.")
        if not product_name or quantity <= 0 or price <= 0:
            raise Exception("Geçersiz ürün bilgileri.")
        order_item = OrderItem.objects.create(order=order, productName=product_name, quantity=quantity, price=price)
        return CreateOrderItem(order_item=order_item)

# Sipariş öğesi güncelleme mutasyonu
class UpdateOrderItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        product_name = graphene.String()
        quantity = graphene.Int()
        price = graphene.Float()

    order_item = graphene.Field(OrderItemType)

    def mutate(self, info, id, product_name=None, quantity=None, price=None):
        try:
            order_item = OrderItem.objects.get(pk=id)
        except OrderItem.DoesNotExist:
            raise Exception("Sipariş öğesi bulunamadı.")
        
        if product_name:
            order_item.productName = product_name
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

    def mutate(self, info, id):
        try:
            order_item = OrderItem.objects.get(pk=id)
            order_item.delete()
            return DeleteOrderItem(success=True)
        except OrderItem.DoesNotExist:
            raise Exception("Sipariş öğesi bulunamadı.")

# Sepete öğe ekleme mutasyonu
class AddCartItem(graphene.Mutation):
    class Arguments:
        user_id = graphene.ID(required=True)
        product_name = graphene.String(required=True)
        quantity = graphene.Int(required=True)
        price = graphene.Float(required=True)

    cart_item = graphene.Field(CartItemType)

    def mutate(self, info, user_id, product_name, quantity, price):
        cart, created = Cart.objects.get_or_create(user_id=user_id)
        cart_item = CartItem.objects.create(
            cart=cart, productName=product_name, quantity=quantity, price=price
        )
        return AddCartItem(cart_item=cart_item)

# Sepet öğesi güncelleme mutasyonu
class UpdateCartItem(graphene.Mutation):
    class Arguments:
        cart_item_id = graphene.ID(required=True)
        quantity = graphene.Int(required=True)

    cart_item = graphene.Field(CartItemType)

    def mutate(self, info, cart_item_id, quantity):
        try:
            cart_item = CartItem.objects.get(pk=cart_item_id)
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

    def mutate(self, info, cart_item_id):
        try:
            cart_item = CartItem.objects.get(pk=cart_item_id)
            cart_item.delete()
            return DeleteCartItem(success=True)
        except CartItem.DoesNotExist:
            raise Exception("Sepet öğesi bulunamadı.")

# Order ve Cart Mutation sınıfı
class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    update_order = UpdateOrder.Field()
    delete_order = DeleteOrder.Field()
    create_order_item = CreateOrderItem.Field()
    update_order_item = UpdateOrderItem.Field()
    delete_order_item = DeleteOrderItem.Field()
    add_cart_item = AddCartItem.Field()
    update_cart_item = UpdateCartItem.Field()
    delete_cart_item = DeleteCartItem.Field()

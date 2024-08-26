import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from users.models import User
from restaurants.models import Restaurant, MenuItem
from orders.models import Order, OrderItem

# UserType tanımlama
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "firstName", "lastName", "email", "birthDate", "isAdmin")

# RestaurantType tanımlama
class RestaurantType(DjangoObjectType):
    class Meta:
        model = Restaurant
        fields = ("id", "name", "address", "phone")

# MenuItemType tanımlama
class MenuItemType(DjangoObjectType):
    class Meta:
        model = MenuItem
        fields = ("id", "name", "description", "price", "restaurant")

# OrderType tanımlama
class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "user", "totalPrice", "createdAt", "updatedAt")

# OrderItemType tanımlama
class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = ("id", "order", "productName", "quantity", "price", "createdAt", "updatedAt")

# Ana Query sınıfı
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_restaurants = graphene.List(RestaurantType)
    all_menu_items = graphene.List(MenuItemType)
    all_orders = graphene.List(OrderType)
    all_order_items = graphene.List(OrderItemType)

    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_all_restaurants(root, info):
        return Restaurant.objects.all()

    def resolve_all_menu_items(root, info):
        return MenuItem.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.all()

    def resolve_all_order_items(root, info):
        return OrderItem.objects.all()

# Schema tanımlama
schema = graphene.Schema(query=Query)

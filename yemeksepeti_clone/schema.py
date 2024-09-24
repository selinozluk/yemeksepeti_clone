import graphene
from graphene_django import DjangoObjectType

from users.models import User
from restaurants.models import Restaurant, MenuItem, MenuItemCategory, RestaurantCategory
from orders.models import Order, OrderItem
from yemeksepeti_clone.decorator import roles_required



# UserType tanımlama
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "firstName", "lastName", "email", "birthDate", "isAdmin")

# RestaurantCategoryType tanımlama (Restoran alanı kaldırıldı)
class RestaurantCategoryType(DjangoObjectType):
    class Meta:
        model = RestaurantCategory
        fields = ("id", "name")

# RestaurantType tanımlama (Kategori alanı kaldırıldı)
class RestaurantType(DjangoObjectType):
    class Meta:
        model = Restaurant
        fields = ("id", "name", "address", "phone", "menu_items")  # menu_items eklendi

    def resolve_menu_items(self, info):
        return self.menu_items.all()

# MenuItemType tanımlama, image alanı eklendi
class MenuItemType(DjangoObjectType):
    class Meta:
        model = MenuItem
        fields = ("id", "name", "description", "price", "restaurant", "category", "image")

    def resolve_image(self, info):
        if self.image:
            return self.image.url
        return None

# OrderType tanımlama
class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        fields = ("id", "user", "totalPrice", "createdAt", "updatedAt", "items")

    def resolve_items(self, info):
        return self.items.all()

# OrderItemType tanımlama
class OrderItemType(DjangoObjectType):
    class Meta:
        model = OrderItem
        fields = ("id", "order", "productName", "quantity", "price", "createdAt", "updatedAt")

# Mutasyon sınıfları

# User Mutasyonları
class CreateUser(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        birth_date = graphene.Date(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, first_name, last_name, email, birth_date, password):
        if User.objects.filter(email=email).exists():
            raise Exception("Bu email adresi zaten kayıtlı.")
        
        user = User.objects.create(
            firstName=first_name,
            lastName=last_name,
            email=email,
            birthDate=birth_date
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)

class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        birth_date = graphene.Date()

    user = graphene.Field(UserType)

    def mutate(self, info, id, first_name=None, last_name=None, email=None, birth_date=None):
        try:
            user = User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Exception("Kullanıcı bulunamadı.")

        if first_name:
            user.firstName = first_name
        if last_name:
            user.lastName = last_name
        if email:
            user.email = email
        if birth_date:
            user.birthDate = birth_date
        user.save()
        return UpdateUser(user=user)

class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @roles_required("ADMIN")
    def mutate(self, info, id):
        try:
            user = User.objects.get(pk=id)
            user.delete()
            return DeleteUser(success=True)
        except User.DoesNotExist:
            raise Exception("Kullanıcı bulunamadı.")

class SignIn(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise Exception("Kullanıcı bulunamadı.")
        
        if not user.check_password(password):
            raise Exception("Geçersiz Parola")

        return SignIn(user=user)

# Restaurant Mutasyonları
class CreateRestaurant(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        address = graphene.String(required=True)
        phone = graphene.String(required=True)

    restaurant = graphene.Field(RestaurantType)

    def mutate(self, info, name, address, phone):
        if not name or not address or not phone:
            raise Exception("Tüm alanlar doldurulmalıdır.")
        
        restaurant = Restaurant.objects.create(name=name, address=address, phone=phone)
        return CreateRestaurant(restaurant=restaurant)

class UpdateRestaurant(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        address = graphene.String()
        phone = graphene.String()

    restaurant = graphene.Field(RestaurantType)

    def mutate(self, info, id, name=None, address=None, phone=None):
        try:
            restaurant = Restaurant.objects.get(pk=id)
        except Restaurant.DoesNotExist:
            raise Exception("Restoran bulunamadı.")

        if name:
            restaurant.name = name
        if address:
            restaurant.address = address
        if phone:
            restaurant.phone = phone
        restaurant.save()
        return UpdateRestaurant(restaurant=restaurant)

class DeleteRestaurant(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            restaurant = Restaurant.objects.get(pk=id)
            restaurant.delete()
            return DeleteRestaurant(success=True)
        except Restaurant.DoesNotExist:
            raise Exception("Restoran bulunamadı.")

# Category Mutasyonları
class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(RestaurantCategoryType)

    def mutate(self, info, name):
        category = RestaurantCategory.objects.create(name=name)
        return CreateCategory(category=category)

class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()

    category = graphene.Field(RestaurantCategoryType)

    def mutate(self, info, id, name=None):
        try:
            category = RestaurantCategory.objects.get(pk=id)
        except RestaurantCategory.DoesNotExist:
            raise Exception("Kategori bulunamadı.")

        if name:
            category.name = name
        category.save()
        return UpdateCategory(category=category)

class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            category = RestaurantCategory.objects.get(pk=id)
            category.delete()
            return DeleteCategory(success=True)
        except RestaurantCategory.DoesNotExist:
            raise Exception("Kategori bulunamadı.")

# MenuItem Mutasyonları
class CreateMenuItem(graphene.Mutation):
    class Arguments:
        restaurant_id = graphene.ID(required=True)
        name = graphene.String(required=True)
        description = graphene.String()
        price = graphene.Float(required=True)
        category_id = graphene.ID(required=True)

    menu_item = graphene.Field(MenuItemType)

    def mutate(self, info, restaurant_id, name, description, price, category_id):
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            raise Exception("Restoran bulunamadı.")
        
        try:
            category = MenuItemCategory.objects.get(pk=category_id)
        except MenuItemCategory.DoesNotExist:
            raise Exception("Kategori bulunamadı.")

        if not name or price <= 0:
            raise Exception("Geçersiz ürün bilgileri.")
        
        menu_item = MenuItem.objects.create(restaurant=restaurant, category=category, name=name, description=description, price=price)
        return CreateMenuItem(menu_item=menu_item)

class UpdateMenuItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        price = graphene.Float()
        category_id = graphene.ID()

    menu_item = graphene.Field(MenuItemType)

    def mutate(self, info, id, name=None, description=None, price=None, category_id=None):
        try:
            menu_item = MenuItem.objects.get(pk=id)
        except MenuItem.DoesNotExist:
            raise Exception("Menü öğesi bulunamadı.")

        if name:
            menu_item.name = name
        if description:
            menu_item.description = description
        if price is not None and price > 0:
            menu_item.price = price
        if category_id:
            try:
                category = MenuItemCategory.objects.get(pk=category_id)
                menu_item.category = category
            except MenuItemCategory.DoesNotExist:
                raise Exception("Kategori bulunamadı.")
        menu_item.save()
        return UpdateMenuItem(menu_item=menu_item)

class DeleteMenuItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            menu_item = MenuItem.objects.get(pk=id)
            menu_item.delete()
            return DeleteMenuItem(success=True)
        except MenuItem.DoesNotExist:
            raise Exception("Menü öğesi bulunamadı.")

# Order Mutasyonları
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

# OrderItem Mutasyonları
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

class DeleteOrderItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @roles_required("STAFF", "ADMIN")
    def mutate(self, info, id):
        try:
            order_item = OrderItem.objects.get(pk=id)
            order_item.delete()
            return DeleteOrderItem(success=True)
        except OrderItem.DoesNotExist:
            raise Exception("Sipariş öğesi bulunamadı.")

# Ana Query ve Mutasyon sınıfları
class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    all_restaurants = graphene.List(RestaurantType)
    all_categories = graphene.List(RestaurantCategoryType)
    all_menu_items = graphene.List(MenuItemType, restaurant_id=graphene.Int())
    all_orders = graphene.List(OrderType)
    all_order_items = graphene.List(OrderItemType)
    restaurant = graphene.Field(RestaurantType, id=graphene.Int(required=True))
    user = graphene.Field(UserType, id=graphene.Int(required=True))

    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_all_restaurants(root, info):
        return Restaurant.objects.all()

    def resolve_all_categories(root, info):
        return RestaurantCategory.objects.all()

    def resolve_all_menu_items(root, info, **kwargs):
        restaurant_id = kwargs.get("restaurant_id")
        items = MenuItem.objects.all()
        if restaurant_id is not None:
            items = items.filter(restaurant_id=restaurant_id)
        return items

    def resolve_all_orders(root, info):
        return Order.objects.all()

    def resolve_all_order_items(root, info):
        return OrderItem.objects.all()

    def resolve_restaurant(root, info, id):
        try:
            return Restaurant.objects.get(pk=id)
        except Restaurant.DoesNotExist:
            raise Exception("Restoran bulunamadı.")

    def resolve_user(root, info, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Exception("Kullanıcı bulunamadı.")

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    sign_in = SignIn.Field()
    create_restaurant = CreateRestaurant.Field()
    update_restaurant = UpdateRestaurant.Field()
    delete_restaurant = DeleteRestaurant.Field()
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
    create_menu_item = CreateMenuItem.Field()
    update_menu_item = UpdateMenuItem.Field()
    delete_menu_item = DeleteMenuItem.Field()
    create_order = CreateOrder.Field()
    update_order = UpdateOrder.Field()
    delete_order = DeleteOrder.Field()
    create_order_item = CreateOrderItem.Field()
    update_order_item = UpdateOrderItem.Field()
    delete_order_item = DeleteOrderItem.Field()

# Schema tanımlama
schema = graphene.Schema(query=Query, mutation=Mutation)

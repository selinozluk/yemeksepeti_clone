import graphene
from graphene_django import DjangoObjectType
from restaurants.models import Restaurant, MenuItem, RestaurantCategory, MenuItemCategory
from yemeksepeti_clone.decorator import roles_required


# Restaurant modelini GraphQL için tanımlama
class RestaurantType(DjangoObjectType):
    class Meta:
        model = Restaurant
        fields = ("id", "name", "address", "phone", "menu_items")


# Menü öğelerini GraphQL için tanımlama
class MenuItemType(DjangoObjectType):
    class Meta:
        model = MenuItem
        fields = ("id", "name", "description", "price", "restaurant", "category", "image")

    def resolve_image(self, info):
        if self.image:
            return info.context.build_absolute_uri(self.image.url)
        return None


# Restoran kategorilerini GraphQL için tanımlama
class RestaurantCategoryType(DjangoObjectType):
    class Meta:
        model = RestaurantCategory
        fields = ("id", "name")


# Sorgular
class Query(graphene.ObjectType):
    # Tüm restoranları listeleme (Kullanıcılar da görebilir)
    all_restaurants = graphene.List(RestaurantType)

    def resolve_all_restaurants(self, info):
        return Restaurant.objects.all()

    # Belirli bir restoranı ID ile getirme (Herkes görebilir)
    restaurant = graphene.Field(RestaurantType, id=graphene.Int(required=True))

    def resolve_restaurant(self, info, id):
        try:
            return Restaurant.objects.get(pk=id)
        except Restaurant.DoesNotExist:
            raise Exception("Restoran bulunamadı.")

    # Menü öğelerini listeleme (Herkes görebilir)
    all_menu_items = graphene.List(MenuItemType, restaurant_id=graphene.Int(required=True))

    def resolve_all_menu_items(root, info, restaurant_id):
        return MenuItem.objects.filter(restaurant_id=restaurant_id)


# Restoran oluşturma mutasyonu (Sadece STAFF ve ADMIN için)
class CreateRestaurant(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        address = graphene.String(required=True)
        phone = graphene.String(required=True)

    restaurant = graphene.Field(RestaurantType)

    @roles_required("STAFF", "ADMIN")
    def mutate(self, info, name, address, phone):
        restaurant = Restaurant.objects.create(name=name, address=address, phone=phone)
        return CreateRestaurant(restaurant=restaurant)


# Restoran güncelleme mutasyonu (Sadece ADMIN için)
class UpdateRestaurant(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        address = graphene.String()
        phone = graphene.String()

    restaurant = graphene.Field(RestaurantType)

    @roles_required("ADMIN")
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


# Restoran silme mutasyonu (Sadece ADMIN için)
class DeleteRestaurant(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @roles_required("ADMIN")
    def mutate(self, info, id):
        try:
            restaurant = Restaurant.objects.get(pk=id)
            restaurant.delete()
            return DeleteRestaurant(success=True)
        except Restaurant.DoesNotExist:
            raise Exception("Restoran bulunamadı.")


# Kategori oluşturma mutasyonu (Sadece STAFF ve ADMIN için)
class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(RestaurantCategoryType)

    @roles_required("STAFF", "ADMIN")
    def mutate(self, info, name):
        category = RestaurantCategory.objects.create(name=name)
        return CreateCategory(category=category)


# Kategori güncelleme mutasyonu (Sadece ADMIN için)
class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()

    category = graphene.Field(RestaurantCategoryType)

    @roles_required("ADMIN")
    def mutate(self, info, id, name=None):
        try:
            category = RestaurantCategory.objects.get(pk=id)
        except RestaurantCategory.DoesNotExist:
            raise Exception("Kategori bulunamadı.")
        if name:
            category.name = name
        category.save()
        return UpdateCategory(category=category)


# Kategori silme mutasyonu (Sadece ADMIN için)
class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @roles_required("ADMIN")
    def mutate(self, info, id):
        try:
            category = RestaurantCategory.objects.get(pk=id)
            category.delete()
            return DeleteCategory(success=True)
        except RestaurantCategory.DoesNotExist:
            raise Exception("Kategori bulunamadı.")


# Menü öğesi oluşturma mutasyonu (Sadece STAFF ve ADMIN için)
class CreateMenuItem(graphene.Mutation):
    class Arguments:
        restaurant_id = graphene.ID(required=True)
        name = graphene.String(required=True)
        description = graphene.String()
        price = graphene.Float(required=True)
        category_id = graphene.ID(required=True)

    menu_item = graphene.Field(MenuItemType)

    @roles_required("STAFF", "ADMIN")
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


# Menü öğesi güncelleme mutasyonu (Sadece STAFF ve ADMIN için)
class UpdateMenuItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        description = graphene.String()
        price = graphene.Float()
        category_id = graphene.ID()

    menu_item = graphene.Field(MenuItemType)

    @roles_required("STAFF", "ADMIN")
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


# Menü öğesi silme mutasyonu (Sadece ADMIN için)
class DeleteMenuItem(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @roles_required("ADMIN")
    def mutate(self, info, id):
        try:
            menu_item = MenuItem.objects.get(pk=id)
            menu_item.delete()
            return DeleteMenuItem(success=True)
        except MenuItem.DoesNotExist:
            raise Exception("Menü öğesi bulunamadı.")


# Mutation sınıfı
class Mutation(graphene.ObjectType):
    create_restaurant = CreateRestaurant.Field()
    update_restaurant = UpdateRestaurant.Field()
    delete_restaurant = DeleteRestaurant.Field()
    create_category = CreateCategory.Field()
    update_category = UpdateCategory.Field()
    delete_category = DeleteCategory.Field()
    create_menu_item = CreateMenuItem.Field()
    update_menu_item = UpdateMenuItem.Field()
    delete_menu_item = DeleteMenuItem.Field()

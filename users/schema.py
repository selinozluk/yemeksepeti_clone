import graphene
from graphene_django import DjangoObjectType
import jwt
from users.models import User
from yemeksepeti_clone.decorator import roles_required
from django.conf import settings

# Kullanıcı modelini GraphQL için tanımlama
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "firstName", "lastName", "email", "birthDate", "isAdmin", "is_customer")

# Sorgular
class Query(graphene.ObjectType):
    # Tüm kullanıcıları listeleme (Sadece STAFF yetkisi olanlar)
    all_users = graphene.List(UserType)

    @roles_required("STAFF")  # Sadece staff kullanıcıları bu sorguyu yapabilir
    def resolve_all_users(root, info):
        return User.objects.all()

    # Belirli bir kullanıcıyı ID ile getirme (STAFF ve CUSTOMER yetkisi olanlar)
    user = graphene.Field(UserType, id=graphene.Int(required=True))

    @roles_required("STAFF", "CUSTOMER")
    def resolve_user(root, info, id):
        user = info.context.user
        # Kullanıcı kendi bilgilerini sorguluyorsa, ona izin veriyoruz
        if user.isAdmin or user.is_staff or user.id == id:
            try:
                return User.objects.get(pk=id)
            except User.DoesNotExist:
                raise Exception("Kullanıcı bulunamadı.")
        raise Exception("Bu işlemi gerçekleştirme yetkiniz yok.")

# Kullanıcı oluşturma mutasyonu (Sadece STAFF yetkisi olanlar)
class CreateUser(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        email = graphene.String(required=True)
        birth_date = graphene.Date(required=True)
        password = graphene.String(required=True)
        is_customer = graphene.Boolean(required=False)  # Müşteri olup olmadığını belirtmek

    user = graphene.Field(UserType)

    @roles_required("STAFF")  # Sadece staff kullanıcıları yeni kullanıcı oluşturabilir
    def mutate(self, info, first_name, last_name, email, birth_date, password, is_customer=False):
        if User.objects.filter(email=email).exists():
            raise Exception("Bu email adresi zaten kayıtlı.")
        user = User.objects.create(
            firstName=first_name,
            lastName=last_name,
            email=email,
            birthDate=birth_date,
            is_customer=is_customer  # Müşteri olup olmadığını ayarla
        )
        user.set_password(password)
        user.save()
        return CreateUser(user=user)

# Kullanıcı güncelleme mutasyonu (STAFF ve kullanıcı kendisi güncelleyebilir)
class UpdateUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        birth_date = graphene.Date()

    user = graphene.Field(UserType)

    @roles_required("STAFF", "CUSTOMER")  # Hem staff hem de kullanıcı kendi bilgilerini güncelleyebilir
    def mutate(self, info, id, first_name=None, last_name=None, email=None, birth_date=None):
        user_requesting = info.context.user
        try:
            user = User.objects.get(pk=id)
            # Eğer kullanıcı admin ya da staff değilse sadece kendi bilgilerini güncelleyebilir
            if not user_requesting.isAdmin and not user_requesting.is_staff and user_requesting.id != id:
                raise Exception("Bu işlemi gerçekleştirme yetkiniz yok.")
        except User.DoesNotExist:
            raise Exception("Kullanıcı bulunamadı.")

        # Kullanıcı bilgilerini güncelleme
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

# Kullanıcı silme mutasyonu (Sadece STAFF yetkisi olanlar)
class DeleteUser(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    @roles_required("STAFF")  # Sadece staff, kullanıcıları silebilir
    def mutate(self, info, id):
        try:
            user = User.objects.get(pk=id)
            user.delete()
            return DeleteUser(success=True)
        except User.DoesNotExist:
            raise Exception("Kullanıcı bulunamadı.")

# Giriş yapma mutasyonu (Herkes için)
class SignIn(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)
    token = graphene.String()

    def mutate(self, info, email, password):
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise Exception("Kullanıcı bulunamadı.")
        if not user.check_password(password):
            raise Exception("Geçersiz Parola")
        payload = {"email": user.email, "exp": 1000000}
        token = jwt.encode(payload, settings.SECRET_KEY, settings.JWT_ALGORITHM)
        return SignIn(user=user, token=token)

# Mutasyonlar
class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    sign_in = SignIn.Field()

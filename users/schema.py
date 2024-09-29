import graphene
from graphene_django import DjangoObjectType
from users.models import User
from yemeksepeti_clone.decorator import roles_required

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "firstName", "lastName", "email", "birthDate", "isAdmin")

class Query(graphene.ObjectType):
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int(required=True))

    def resolve_all_users(root, info):
        return User.objects.all()

    def resolve_user(root, info, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Exception("Kullanıcı bulunamadı.")

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

class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()
    sign_in = SignIn.Field()
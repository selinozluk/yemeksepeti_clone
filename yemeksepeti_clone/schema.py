import graphene
from users.schema import Query as UsersQuery, Mutation as UsersMutation
from restaurants.schema import Query as RestaurantsQuery, Mutation as RestaurantsMutation
from orders.schema import Query as OrdersQuery, Mutation as OrdersMutation

# Tüm Query'leri birleştirme
class Query(UsersQuery, RestaurantsQuery, OrdersQuery, graphene.ObjectType):
    pass

# Tüm Mutation'ları birleştirme
class Mutation(UsersMutation, RestaurantsMutation, OrdersMutation, graphene.ObjectType):
    pass

# Schema tanımı
schema = graphene.Schema(query=Query, mutation=Mutation)


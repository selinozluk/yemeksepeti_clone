import graphene
from users.schema import Query as UsersQuery, Mutation as UsersMutation
from restaurants.schema import Query as RestaurantsQuery, Mutation as RestaurantsMutation
from orders.schema import OrderType, OrderItemType, CartType, CartItemType


class Query(UsersQuery, RestaurantsQuery, graphene.ObjectType):
    pass

class Mutation(UsersMutation, RestaurantsMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

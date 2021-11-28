import graphene

import api.schema as schema
import api.schema_user as schema_user



class Query(schema_user.Query,schema.Query, graphene.ObjectType):
    pass

class Mutation(schema_user.Mutation,schema.Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

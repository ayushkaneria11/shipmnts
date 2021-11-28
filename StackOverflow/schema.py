import graphene

import api.schema as schema
import api.schema_user as schema_user
import graphql_jwt



class Query(schema_user.Query,schema.Query, graphene.ObjectType):
    pass

class Mutation(schema_user.Mutation,schema.Mutation, graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)

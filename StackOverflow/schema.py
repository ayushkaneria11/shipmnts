import graphene

import api.schema as schema



class Query(schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)

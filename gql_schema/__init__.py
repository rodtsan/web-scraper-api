# flask_sqlalchemy/schema.py
import os
import graphene
from graphene import Schema
from graphql import GraphQLError
from .mutations import CreateProfile, DeleteProfile, CreateTopic
from .queries import (
    ProfileObject,
    PostObject,
    TopicObject,
    SearchResult,
    find_similarites,
)


class Query(graphene.ObjectType):
    # node = graphene.relay.Node.Field()
    # Allows sorting over multiple columns, by default over the primary key
    profiles = graphene.List(ProfileObject)

    def resolve_profiles(self, info):
        return ProfileObject.get_query(info).all()

    topics = graphene.List(TopicObject)

    def resolve_topics(self, info):
        return TopicObject.get_query(info).all()

    symantic_search = graphene.List(
        SearchResult,
        search_input=graphene.String(required=True),
        csv_file=graphene.String(required=True),
    )

    def resolve_symantic_search(self, _, search_input=None, csv_file=None):
        if not csv_file:
            cvs_filepath = f"{os.getcwd()}/files/embeddings/{csv_file}"
            if not os.path.exists(cvs_filepath):
                raise GraphQLError(f"File {csv_file} not found")
        return [SearchResult(**sr) for sr in find_similarites(search_input, csv_file)]


class Mutation(graphene.ObjectType):
    create_profile = CreateProfile.Field()
    delete_profile = DeleteProfile.Field()
    create_topic = CreateTopic.Field()


schema = Schema(
    query=Query,
    mutation=Mutation,
    types=[ProfileObject, PostObject, TopicObject, CreateProfile, CreateTopic, DeleteProfile, SearchResult],
    auto_camelcase=False,
)

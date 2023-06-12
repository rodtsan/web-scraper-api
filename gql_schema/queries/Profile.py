
from graphene_sqlalchemy import SQLAlchemyObjectType
from data.models import Profile, Post


class ProfileObject(SQLAlchemyObjectType):
    class Meta:
        name = "profiles"
        model = Profile
        # interfaces = (relay.Node, ProfileType)


class PostObject(SQLAlchemyObjectType):
    class Meta:
        name = "posts"
        model = Post
        # interfaces = (relay.Node, PostType)
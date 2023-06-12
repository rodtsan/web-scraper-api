
from graphene_sqlalchemy import SQLAlchemyObjectType
from data.models import Topic


class TopicObject(SQLAlchemyObjectType):
    class Meta:
        name = "topics"
        model = Topic
        # interfaces = (relay.Node, PostType)
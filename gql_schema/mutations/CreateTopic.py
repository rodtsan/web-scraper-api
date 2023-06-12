import graphene
from graphql import GraphQLError
from data.models import Topic, session
from gql_schema.queries import TopicObject


class TopicInput(graphene.InputObjectType):
    title = graphene.String(required=True)
    csv_file = graphene.String(required=True)
    search_title = graphene.String()
    search_text = graphene.String()


class CreateTopic(graphene.Mutation):
    class Arguments:
        topic_input = TopicInput(required=True)

    topic = graphene.Field(TopicObject)

    def mutate(self, info, topic_input=None):
        update_topic = (
            session.query(Topic).where(Topic.csv_file == topic_input.csv_file).first()
        )
        if update_topic == None:
            new_topic = Topic(**topic_input)
            session.add(new_topic)
            session.commit()
            return CreateTopic(topic=new_topic)
        else:
            session.query(Topic).filter(Topic.id == update_topic.id).update(
                {
                    "title": topic_input.title,
                    "search_title": topic_input.search_title,
                    "search_text": topic_input.search_text,
                }
            )
            session.commit()
            return CreateTopic(topic=update_topic)

import graphene
from graphql import GraphQLError
from data.models import Profile, session

class DeletedProfile(graphene.ObjectType):
    name = graphene.String()
    description = graphene.String()
    link = graphene.String()


class DeleteProfile(graphene.Mutation):
    class Arguments:
        id = graphene.String(required=True)

    profile = graphene.Field(DeletedProfile)

    def mutate(self, info, id=None):
        profile_to_be_deleted = (
            session.query(Profile).where(Profile.id == id).first()
        )
        if profile_to_be_deleted == None:
            raise GraphQLError(message="Profile record not found")
        else:
            deleted_profile = {
                "name": profile_to_be_deleted.name,
                "description": profile_to_be_deleted.description,
                "link": profile_to_be_deleted.link,
            }
            session.delete(profile_to_be_deleted)
            session.commit()
            return DeleteProfile(
                profile=deleted_profile,
                message="Profile has successfully deleted",
                success=True,
            )

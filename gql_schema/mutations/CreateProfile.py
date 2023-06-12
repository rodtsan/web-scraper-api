import graphene
from utils.linkedin_scraper import LinkedInScraper
from data.models import Post, Profile, session

class CreateProfile(graphene.Mutation):
    class Post(graphene.ObjectType):
        id = graphene.ID()
        name = graphene.String()
        description = graphene.String()
        posted_by = graphene.String()
        comments = graphene.String()
        date_posted = graphene.String()

    id = graphene.ID()
    name = graphene.String()
    description = graphene.String()
    email = graphene.String()
    link = graphene.String()
    date_added = graphene.String()
    posts = graphene.List(Post)

    success = graphene.Boolean()

    class Arguments:
        url = graphene.String(required=True)

    def mutate(self, info, url=None):
        web_scraper = LinkedInScraper(url)
        results = web_scraper.get_data()
        profile = session.query(Profile).where(Profile.name == results["name"]).first()
        if profile == None:
            profile_dict = {k: v for k, v in results.items() if k != "posts"}
            new_profile = Profile(
                **profile_dict,
                posts=[Post(**post) for post in results["posts"]],
            )
            session.add(new_profile)
            session.commit()
            return CreateProfile(**results, success=True)
        else:
            dict_posts = results["posts"]
            if len(dict_posts) > 0:
                if len(profile.posts) > 0:
                    saved_comments = [post.comments[0:100] for post in profile.posts]
                    dict_new_posts = []
                    for dict_post in dict_posts:
                        post_message = dict_post["comments"]
                        strip_post_message = post_message[0:20].strip()
                        if not any(
                            strip_post_message in saved_comment
                            for saved_comment in saved_comments
                        ):
                            dict_new_posts.append(dict_post)

                        if len(dict_new_posts) > 0:
                            new_posts = [
                                Post(
                                    **post,
                                    profile_id=profile.id,
                                )
                                for post in dict_new_posts
                            ]
                            session.add_all(new_posts)
                            session.commit()
                else:
                    new_posts = [
                        Post(**post, profile_id=profile.id) for post in dict_posts
                    ]
                    session.add_all(new_posts)
                    session.commit()

            return CreateProfile(**profile.to_dict(), success=True)

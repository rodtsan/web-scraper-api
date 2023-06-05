from app import app, db
from flask import jsonify
from Schema import Post
from sqlalchemy.orm import Session

def __map_post(post: Post) -> dict[str, any]:
    return {
        "name": post.name,
        "description": post.description,
        "posted_by": post.posted_by,
        "comments": post.comments,
        "date_posted": post.date_posted,
    }

@app.route("/api/linkedin/profile-posts")
@app.route("/api/linkedin/profile-posts/<post_id>")
async def get_posts_by_profile(profile_id=None):
    engine = db.get_engine()
    if profile_id:
        with Session(engine) as session:
            posts = session.query(Post).where(Post.profile_id == profile_id).all()
            posts_list = [
                __map_post(post)
                for post in posts
            ]
            session.close()
            return jsonify(posts_list)
    else:
        with Session(engine) as session:
            posts = session.query(Post).order_by(Post.date_posted).all()
            posts_list = [
                __map_post(post)
                for post in posts
            ]
            session.close()
            return jsonify(posts_list)

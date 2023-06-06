from app import app, db
from flask import Blueprint, Response, abort, json, request, jsonify
from data.Schema import Post
from sqlalchemy.orm import Session

# def __map_post(post: Post) -> dict[str, any]:
#     return {
#         "name": post.name,
#         "description": post.description,
#         "posted_by": post.posted_by,
#         "comments": post.comments,
#         "date_posted": post.date_posted,
#     }


@app.route("/api/linkedin/posts")
@app.route("/api/linkedin/posts/<post_id>", methods=["GET", "DELETE"])
async def get_posts(post_id:int=0):
    engine = db.get_engine()
    match request.method:
        case "GET":
            if int(post_id) > 0:
                with Session(engine) as session:
                    post = session.query(Post).where(Post.id == post_id).first()
                    post_dict = post.to_dict()
                    session.close()
                    return jsonify(post_dict)
            else:
                with Session(engine) as session:
                    posts = session.query(Post).order_by(Post.date_posted).all()
                    posts_list = [
                        post.to_dict()
                        for post in posts
                    ]
                    session.close()
                    return jsonify(posts_list)
        case "DELETE":
            with Session(engine) as session:
                post = session.query(Post).where(Post.id == post_id).first()
                if post:
                    session.delete(post)
                    session.commit()
                    session.close()
                    return jsonify(
                        {"message": f"Post id {post_id} has successfully deleted."}
                    )
                else:
                    session.close()
                    return Response(
                        json.dumps({"error": "Record post cannot be found"}),
                        status=422,
                        mimetype="application/json",
                    )
        case _:
            abort(405)
from app import app, db
from flask import Response, abort, json, request, jsonify
from Schema import Profile, Post
from sqlalchemy.orm import Session


def __map_profile(profile: Profile) -> dict[str, any]:
    return {
        "id": profile.id,
        "name": profile.name,
        "email": profile.email,
        "description": profile.description,
        "link": profile.link,
        "date_added": profile.date_added,
        "posts": [
            {
                "name": post.name,
                "description": post.description,
                "posted_by": post.posted_by,
                "comments": post.comments,
                "date_posted": post.date_posted,
            }
            for post in profile.posts
        ],
    }


@app.route("/api/linkedin/profiles")
@app.route("/api/linkedin/profiles/<profile_id>", methods=["GET", "DELETE"])
def get_profiles(profile_id: int = 0):
    engine = db.get_engine()
    match request.method:
        case "GET":
            if int(profile_id) > 0:
                with Session(engine) as session:
                    profile = (
                        session.query(Profile).where(Profile.id == profile_id).first()
                    )
                    profile_dict = __map_profile(profile)
                    session.close()
                    return jsonify(profile_dict)
            else:
                with Session(engine) as session:
                    profiles = session.query(Profile).order_by(Profile.date_added).all()
                    profiles_list = [__map_profile(profile) for profile in profiles]
                    session.close()
                    return jsonify(profiles_list)
        case "DELETE":
            with Session(engine) as session:
                profile = session.query(Profile).where(Profile.id == profile_id).first()
                if profile:
                    session.delete(profile)
                    session.commit()
                    session.close()
                    return jsonify(
                        {"message": f"Profile id {profile_id} has successfully deleted."}
                    )
                else:
                    session.close()
                    return Response(
                        json.dumps({"error": "Record profile cannot be found"}),
                        status=422,
                        mimetype="application/json",
                    )
        case _:
            abort(405)

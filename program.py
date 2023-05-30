import re
from flask import Flask, jsonify, request
from flask_cors import CORS
from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup, SoupStrainer
import chromedriver_binary
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select, exists
from Shema import *

app = Flask(__name__)
CORS(app)

engine = create_engine("sqlite:///sm_db.db", echo=True)
Base.metadata.create_all(engine)


@app.route("/api/")
def main():
    return jsonify({"status": "healty"})


@app.route("/api/linkedin")
def get_linkedin_data():
    options = webdriver.ChromeOptions()
    # options.add_argument(
    #     "--user-data-dir=C:/Users/Rodrigo/AppData/Local/Google/Chrome/User Data"
    # )
    # options.add_argument("--profile-directory=Default")
    # options.add_argument("--ignore-certificate-errors")
    # options.add_argument('--incognito')
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.linkedin.com/")

    sleep(2)
    request_url = request.args.get("url")
    linkedin_url = request_url
    if request_url[len(request_url) - 1] == "/":
        linkedin_url = request_url + "recent-activity/all/"
    else:
        linkedin_url = request_url + "/recent-activity/all/"

    driver.get(linkedin_url)
    sleep(2)

    current_posts = []
    error_message = ""
    profile_desc = ""
    profile_name = ""
    current_url = driver.current_url
    # check current url whether redirected other page
    if re.search("/recent-activity/", current_url):
        try:
            parse_only = SoupStrainer(id="profile-content")
            bs = BeautifulSoup(driver.page_source, "lxml", parse_only=parse_only)

            sider_bar = bs.find("div", class_="scaffold-layout__sidebar")
            sider_bar_inner = sider_bar.find('div', id="recent-activity-top-card")
            
            profile_name = sider_bar_inner.find("h3").get_text().strip()
            profile_desc = sider_bar_inner.find("h4").get_text().strip()

            main_content = bs.find("main", class_="scaffold-layout__main")
            recent_activities = main_content.find_all(
                "li", class_="profile-creator-shared-feed-update__container"
            )
            limit = 5
            index = 1
            for element in recent_activities:
                posted_by = ""
                comments = ""
                try:
                    re_posted_element = meta_element.find(
                        "div", class_="update-components-text-view"
                    )
                    re_posted_by = re_posted_element.find("span").find("a")
                    posted_by = re_posted_by.get_text()
                except:
                    pass
                try:
                    comment_element = element.find(
                        "div", class_="update-components-text"
                    ).find("span")
                    comments = comment_element.get_text()
                except:
                    pass
                meta_element = element.find(
                    "div", class_="update-components-actor__meta"
                )
                author_name_element = (
                    meta_element.find(
                        "span", class_="update-components-actor__title"
                    )
                    .find("span")
                    .find("span")
                )
                author_desc_element = meta_element.find(
                    "span", class_="update-components-actor__description"
                ).find("span")
                author_name = author_name_element.get_text()
                author_desc = author_desc_element.get_text()

                date_posted = (
                    meta_element.find(
                        "span", class_="update-components-actor__sub-description"
                    )
                    .find("div")
                    .find("span")
                    .find("span", class_="visually-hidden")
                ).get_text()
                print(f"activity: {index}")
                current_posts.append(
                    {
                        "post_id": index,
                        "posted_by": posted_by,
                        "name": author_name,
                        "description": author_desc,
                        "date_posted": date_posted,
                        "comments": comments,
                    }
                )
                sleep(2)
                index += 1
                if index == limit:
                    break

        except Exception as ex:
            print(f'{ex.args.__repr__()}')
            pass
    else:
        error_message = f"Wrong url source {current_url}"

    driver.close()

    if bool(error_message):
        return jsonify({"error": error_message})
    else:
        if len(current_posts) > 0:
            try:
                with Session(engine) as session:
                    query = select(Profile).where(Profile.name == profile_name.strip())
                    profile = session.scalar(query)
                    now = datetime.now()
                    if profile == None:
                        print("null")
                        posts = [
                            Post(
                                name=post.get("name"),
                                description=post.get("description"),
                                posted_by=post.get("posted_by"),
                                comments=post.get("comments"),
                                date_posted=post.get("date_posted"),
                            )
                            for post in current_posts
                        ]

                        profile = Profile(
                            name=profile_name,
                            description=profile_desc,
                            link=request_url,
                            email="",
                            date_added=now.strftime("%m/%d/%Y, %H:%M:%S"),
                            posts=posts,
                        )
                        session.add(profile)
                        session.commit()
                    else:
                        print("not null")
                        if len(profile.posts) > 0:
                            saved_comments = [post.comments for post in profile.posts]
                            new_posts = []
                            for post_comment_dict in current_posts:
                                post_comment = post_comment_dict.get("comments")
                                if len(post_comment) > 15:
                                    if not [
                                        post_comment[0:15].strip() in saved_comments
                                    ]:
                                        new_posts.append(post_comment_dict)
                                else:
                                    if not [post_comment in saved_comments]:
                                        new_posts.append(post_comment_dict)

                            if len(new_posts) > 0:
                                session.add_all(posts)
                                session.commit()

                        else:
                            posts = [
                                Post(
                                    name=post.get("name"),
                                    description=post.get("description"),
                                    comments=post.get("comments"),
                                    posted_by=post.get("posted_by"),
                                    profile_id=profile.id,
                                    profile=profile,
                                    date_posted=post.get("date_posted"),
                                )
                                for post in current_posts
                            ]
                            session.add_all(posts)
                            session.commit()

                    session.close()
            except Exception as ex:
                return jsonify({"error": ex.args.__repr__()})
    return jsonify(
        {"name": profile_name, "description": profile_desc, "link": request_url, "posts": current_posts}
    )


@app.route("/api/linkedin/authors")
def get_linkedin_authors():
    profiles = []
    try:
        with Session(engine) as session:
            results = session.query(Profile).order_by(Profile.date_added).all()
            profiles = [
                {
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
                for profile in results
            ]
            session.close()

    except Exception as ex:
        return jsonify({"error": ex.args.__repr__()})

    return jsonify(profiles)


if __name__ == "__main__":
    app.run(port=8000)

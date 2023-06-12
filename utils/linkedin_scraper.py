# Import Libraries
import re
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup, SoupStrainer
from flask import jsonify, make_response, request
from selenium import webdriver

class LinkedInScraper:
    def __init__(self, linkedin_url: str | None):
        self.url = linkedin_url
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(
            "--user-data-dir=C:/Users/Rodrigo/AppData/Local/Google/Chrome/User Data/"
        )
        self.options.add_argument("--profile-directory=Default")
        self.options.add_argument("--ignore-certificate-errors")
        self.options.add_argument("--headless")
        self.options.add_argument("--log-level=3")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-infobars")

    def __get_link(self):
        if self.url[len(self.url) - 1] == "/":
            return self.url + "recent-activity/all/"
        else:
            return self.url + "/recent-activity/all/"

    def get_data(self) -> dict[str, any]:
        driver = webdriver.Chrome(options=self.options)
        driver.get("https://www.linkedin.com/")
        sleep(2)
        linkedin_url = self.__get_link()
        driver.get(linkedin_url)
        sleep(2)
        current_posts = []
        profile_desc = ""
        profile_name = ""
        current_url = driver.current_url
        # check current url whether redirected other page
        if re.search("/recent-activity/", current_url):
            try:
                parse_only = SoupStrainer(id="profile-content")
                bs = BeautifulSoup(driver.page_source, "lxml", parse_only=parse_only)

                sider_bar = bs.find("div", class_="scaffold-layout__sidebar")
                sider_bar_inner = sider_bar.find("div", id="recent-activity-top-card")

                profile_name = sider_bar_inner.find("h3").get_text().strip()
                profile_desc = sider_bar_inner.find("h4").get_text().strip()

                main_content = bs.find("main", class_="scaffold-layout__main")
                recent_activities = main_content.find_all(
                    "li", class_="profile-creator-shared-feed-update__container"
                )
                for element in recent_activities:
                    posted_by = ""
                    comments = ""
                    author_name = ""
                    author_desc = ""
                    date_posted = ""
                    try:
                        posted_by = (
                            meta_element.find(
                                "div", class_="update-components-text-view"
                            )
                            .find("span")
                            .find("a")
                            .get_text()
                        )
                    except:
                        pass
                    try:
                        comments = (
                            element.find("div", class_="update-components-text")
                            .find("span")
                            .get_text()
                        )
                    except:
                        pass
                    meta_element = element.find(
                        "div", class_="update-components-actor__meta"
                    )
                    try:
                        author_name = (
                            meta_element.find(
                                "span", class_="update-components-actor__title"
                            )
                            .find("span")
                            .find("span")
                        ).get_text()
                    except:
                        pass
                    try:
                        author_desc = (
                            meta_element.find(
                                "span", class_="update-components-actor__description"
                            )
                            .find("span")
                            .get_text()
                        )
                    except:
                        pass
                    try:
                        date_posted = (
                            meta_element.find(
                                "span",
                                class_="update-components-actor__sub-description",
                            )
                            .find("div")
                            .find("span")
                            .find("span", class_="visually-hidden")
                        ).get_text()
                    except:
                        pass
                    if len(comments) > 10:
                        current_posts.append(
                            {
                                "name": author_name,
                                "description": author_desc,
                                "posted_by": posted_by,
                                "date_posted": date_posted,
                                "comments": comments,
                            }
                        )
                    sleep(2)
            except Exception as error:
                raise error
        driver.close()
        return {
            "name": profile_name,
            "description": profile_desc,
            "link": current_url,
            "posts": current_posts,
        }

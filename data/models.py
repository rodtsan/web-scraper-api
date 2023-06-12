from datetime import datetime
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from sqlalchemy.orm import relationship

engine = create_engine(
    "sqlite:///sm_db.db", convert_unicode=True
)  # echo=True sql event logs
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
# We will need this for querying

Base.query = session.query_property()


class Profile(Base):
    __tablename__ = "linkedin_profile"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    description = Column(String(255))
    link = Column(String(128))
    email = Column(String(128))
    date_added = Column(DateTime, default=datetime.utcnow)
    posts = relationship("Post", back_populates="profile", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "link": self.link,
            "email": self.email,
            "date_added": self.date_added,
            "posts": [
                {
                    "id": post.id,
                    "name": post.name,
                    "description": post.description,
                    "posted_by": post.posted_by,
                    "comments": post.comments,
                    "date_posted": post.date_posted,
                }
                for post in self.posts
            ],
        }


class Post(Base):
    __tablename__ = "linkedin_post"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    description = Column(String(255))
    comments = Column(Text)
    profile_id = Column(Integer, ForeignKey("linkedin_profile.id"))
    profile = relationship("Profile", back_populates="posts")
    posted_by = Column(String(128))
    date_posted = Column(String(28))
    date_added = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "profile_id": self.profile_id,
            "comments": self.comments,
            "posted_by": self.posted_by,
            "date_posted": self.date_posted,
        }


class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    csv_file = Column(String(128))
    search_title = Column(String(255))
    search_text = Column(String(500))
    date_added = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "csv_file": self.csv_file,
            "search_title": self.search_title,
            "search_text": self.search_text,
        }

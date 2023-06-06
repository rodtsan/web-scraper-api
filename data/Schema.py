# from typing import List
# from typing import Optional
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from app import app, db
# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime

# engine = create_engine('sqlite:///database.sqlite3', convert_unicode=True)
# db_session = scoped_session(sessionmaker(autocommit=False,
#                                          autoflush=False,
#                                          bind=engine))


Base = declarative_base()
# class Base(DeclarativeBase):
#    pass


class Profile(Base):
    __tablename__ = "linkedin_profile"

    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    description = Column(String(255))
    link = Column(String(128))
    email = Column(String(128))
    date_added = Column(String(32))
    posts = relationship("Post", back_populates="profile", cascade="all, delete-orphan")

    # id: Mapped[int] = mapped_column(primary_key=True)
    # link: Mapped[str] = mapped_column(String(255))
    # email: Mapped[Optional[str]]
    # name: Mapped[Optional[str]]
    # description: Mapped[Optional[str]]
    # date_added: Mapped[Optional[str]]
    # posts: Mapped[List["Post"]] = relationship(
    #     back_populates="profile", cascade="all, delete-orphan"
    # )

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
    profile = relationship(Profile, back_populates="posts")
    posted_by = Column(String(128))
    date_posted = Column(String(28))

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

    # id: Mapped[int] = mapped_column(primary_key=True)
    # profile_id: Mapped[int] = mapped_column(ForeignKey("linkedin_profile.id"))
    # profile: Mapped["Profile"] = relationship(back_populates="posts")
    # posted_by: Mapped[Optional[str]]
    # name: Mapped[Optional[str]]
    # description: Mapped[Optional[str]]
    # comments: Mapped[Optional[str]]
    # date_posted: Mapped[Optional[str]]

    # def __repr__(self) -> str:
    #     return f"Post(id={self.id!r}, email={self.email!r})"

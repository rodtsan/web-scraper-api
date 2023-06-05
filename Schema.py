from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from datetime import datetime


class Base(DeclarativeBase):
   pass

class Profile(Base):
    __tablename__ = "linkedin_profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column(String(255))
    email: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    date_added: Mapped[Optional[str]]
    posts: Mapped[List["Post"]] = relationship(
        back_populates="profile", cascade="all, delete-orphan"
    )

def __repr__(self) -> str:
    return f"Profile(id={self.id!r}, link={self.link!r}, name={self.name!r})"

class Post(Base):
    __tablename__ = "linkedin_post"

    id: Mapped[int] = mapped_column(primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("linkedin_profile.id"))
    profile: Mapped["Profile"] = relationship(back_populates="posts")
    posted_by: Mapped[Optional[str]]
    name: Mapped[Optional[str]]
    description: Mapped[Optional[str]]
    comments: Mapped[Optional[str]]
    date_posted: Mapped[Optional[str]]

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, email={self.email!r})"

    
    

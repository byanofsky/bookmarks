from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from bookmarks.database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(120))
    email = Column(String(256), unique=True, nullable=False)

    bookmarks = relationship("Bookmark", back_populates="user")

    def __init__(self, username=None, name=None, email=None):
        self.username = username
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)


class Bookmark(Base):
    __tablename__ = 'bookmark'
    id = Column(Integer, primary_key=True)
    short = Column(String(6), unique=True, nullable=False)
    link = Column(Text, nullable=False)
    hits = Column(BIGINT(unsigned=True))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="bookmarks")

    def __init__(self, short, link):
        self.short = short
        self.link = link
        self.hits = 0

    def __repr__(self):
        return '<Bookmark %r>' % (self.short)

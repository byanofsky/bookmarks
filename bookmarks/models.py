from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from bookmarks.database import Base
from bookmarks import bcrypt


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(120))
    email = Column(String(256), unique=True, nullable=False)
    pw_hash = Column(String(60), nullable=False)

    bookmarks = relationship("Bookmark", back_populates="user")

    def __init__(self, username, name, email, password):
        self.username = username
        self.name = name
        self.email = email
        self.pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def __repr__(self):
        return '<User %r>' % (self.username)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.pw_hash, password)


class Bookmark(Base):
    __tablename__ = 'bookmark'
    id = Column(Integer, primary_key=True)
    short = Column(String(6), unique=True, nullable=False)
    link = Column(Text, nullable=False)
    hits = Column(BIGINT(unsigned=True))

    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", back_populates="bookmarks")

    def __init__(self, short, link, user_id):
        self.short = short
        self.link = link
        self.hits = 0
        self.user_id = user_id

    def __repr__(self):
        return '<Bookmark %r>' % (self.short)

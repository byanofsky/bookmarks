from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from bookmarks.database import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(120))
    email = Column(String(256), unique=True, nullable=False)

    bookmarks = relationship("Bookmark", back_populates="user")

    def __init__(self, name=None, username=None, email=None):
        self.username = username
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

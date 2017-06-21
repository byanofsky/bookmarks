from sqlalchemy import Column, Integer, String
from bookmarks.database import Base


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    name = Column(String(120))
    email = Column(String(256), unique=True, nullable=False)

    def __init__(self, name=None, username=None, email=None):
        self.username = username
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r>' % (self.name)

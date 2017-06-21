from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import relationship
from bookmarks.database import Base


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

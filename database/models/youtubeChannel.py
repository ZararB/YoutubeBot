from database.models.base import Base
from sqlalchemy import Column, Integer, String


class YoutubeChannel(Base):
    __tablename__ = 'youtubeChannel'

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    uniqueId = Column(String)
    followerCount = Column(Integer)
    contentCount = Column(Integer)
    averageViewCount = Column(Integer)

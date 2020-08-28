from database.models.base import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func


class YoutubeChannel(Base):
    __tablename__ = 'YoutubeChannels'

    Id = Column(Integer, primary_key=True)
    Url = Column(String)
    Nickname = Column(String)
    SearchTerm = Column(Integer, nullable=True)
    SearchTermViews = Column(String, nullable=True)
    CreatedAt = Column(TIMESTAMP, server_default=func.now())
    ScrapedAt = Column(TIMESTAMP, nullable=True)
    DeletedAt = Column(TIMESTAMP, nullable=True)

    def __init__(self,
                 url=None,
                 nickname=None,
                 searchterm=None,
                 searchterm_views=None,
                 scraped_at=None):
        self.Url = url
        self.Nickname = nickname
        self.SearchTerm = searchterm
        self.SearchTermViews = searchterm_views
        self.ScrapedAt = scraped_at
        pass

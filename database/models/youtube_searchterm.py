from database.models.base import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func


class YoutubeSearchTerm(Base):
    __tablename__ = 'YoutubeSearchTerms'

    Id = Column(Integer, primary_key=True)
    Term = Column(String)
    CreatedAt = Column(TIMESTAMP, server_default=func.now())

    def __init__(self,
                 term=None):
        self.Term = term
        pass

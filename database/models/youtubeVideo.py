from database.models.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from database.models.youtubeChannel import YoutubeChannel


class YoutubeVideo(Base):
    __tablename__ = 'youtubeVideo'

    id = Column(Integer, primary_key=True)
    channelId = Column(Integer, ForeignKey(YoutubeChannel.id))
    title = Column(String)
    desc = Column(String)
    thumbnailFileLocation = Column(String)


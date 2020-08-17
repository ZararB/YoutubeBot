from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from tiktok.tiktokChannel import TiktokChannel
from youtube.youtubeChannel import YoutubeChannel

engine = create_engine('postgresql://postgres:wabbalabba@localhost/youtubebot', echo=True)
Base = declarative_base(engine)



class YoutubeVideo(Base):

    __tablename__ = 'youtubeVideo'

    id = Column(Integer, primary_key=True)
    channelId = Column(Integer, ForeignKey(YoutubeChannel.id))
    title = Column(String)
    desc = Column(String)
    thumbnailFileLocation = Column(String)

	




Base.metadata.create_all(engine)






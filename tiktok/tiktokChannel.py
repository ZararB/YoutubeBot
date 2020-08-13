from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String



engine = create_engine('postgresql://postgres:wabbalabba@localhost/youtubebot', echo=True)
Base = declarative_base(engine)

class TiktokChannel(Base):

    __tablename__ = 'tiktokChannel'
    

    uniqueId = Column(String, primary_key=True)
    nickname = Column(String)
    followerCount = Column(Integer)
    followingCount = Column(Integer)
    heartCount = Column(Integer)
    videoCount = Column(Integer)

    def channelFromChannelDict(channelDict):
        channel = TiktokChannel()
        channel.uniqueId = channelDict['userInfo']['user']['uniqueId']
        channel.nickname = channelDict['userInfo']['user']['nickname']
        channel.followerCount = channelDict['userInfo']['stats']['followerCount']
        channel.followingCount = channelDict['userInfo']['stats']['followingCount']
        channel.heartCount = channelDict['userInfo']['stats']['heartCount']
        channel.videoCount = channelDict['userInfo']['stats']['videoCount']
        
        return channel

Base.metadata.create_all(engine)
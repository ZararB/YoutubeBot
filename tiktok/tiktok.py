from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from tiktokChannel import TiktokChannel


engine = create_engine('postgresql://postgres:wabbalabba@localhost/youtubebot', echo=True)
Base = declarative_base(engine)



class Tiktok(Base):

    __tablename__ = 'tiktoks'

    id = Column(Integer, primary_key=True)
    tiktokId = Column(String)
    channelUniqueId = Column(String, ForeignKey(TiktokChannel.uniqueId))
    desc = Column(String)
    diggCount = Column(Integer)
    playCount = Column(Integer)
    commentCount = Column(Integer)
    fileLocation = Column(String)
    duration = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    songName = Column(String)
    songId = Column(String)


    def tiktokFromTiktokDict(tiktokDict, fileLocation):
        tiktok = Tiktok()
        tiktok.tiktokId = tiktokDict['id']
        tiktok.channelUniqueId = tiktokDict['author']['uniqueId'] 
        tiktok.desc = tiktokDict['desc']
        tiktok.diggCount = tiktokDict['stats']['diggCount']
        tiktok.playCount = tiktokDict['stats']['playCount']
        tiktok.commentCount = tiktokDict['stats']['commentCount']
        tiktok.shareCount = tiktokDict['stats']['shareCount']
        tiktok.fileLocation = fileLocation
        tiktok.duration = tiktokDict['video']['duration']
        tiktok.width = tiktokDict['video']['width']
        tiktok.height = tiktokDict['video']['height']
        tiktok.songName = tiktokDict['music']['title']
        tiktok.songId = tiktokDict['music']['id']

        return tiktok

        





Base.metadata.create_all(engine)






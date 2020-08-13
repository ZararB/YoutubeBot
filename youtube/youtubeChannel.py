from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String



engine = create_engine('sqlite:///data/databases/memes2.db', echo=True)
Base = declarative_base(engine)

class YoutubeChannel(Base):

    __tablename__ = 'youtubeChannel'
    

    id = Column(Integer, primary_key=True)
    nickname = Column(String)
    uniqueId = Column(String)
    followerCount = Column(Integer)
    contentCount = Column(Integer)
    averageViewCount = Column(Integer)




Base.metadata.create_all(engine)
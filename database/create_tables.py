from database.models.base import Base
from database.connection import engine

# import models
from database.models.tiktok import Tiktok
from database.models.tiktokChannel import TiktokChannel
from database.models.youtubeChannel import YoutubeChannel
from database.models.youtubeVideo import YoutubeVideo

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)

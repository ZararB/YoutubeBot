from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tiktok import *


engine = create_engine('postgresql://postgres:wabbalabba@localhost/youtubebot', echo=True)
Session = sessionmaker(bind = engine)



class Creator:


    def __init__(self):
        self.session = Session()



from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey


engine = create_engine('sqlite:///data/databases/memes2.db', echo=True)
Base = declarative_base(engine)



class Instagram(Base):

    __tablename__ = 'instagram'

    id = Column(Integer, primary_key=True)
    




Base.metadata.create_all(engine)






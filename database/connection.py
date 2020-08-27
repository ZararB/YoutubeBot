from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# dev database connection
dbuser = 'postgres'
dbpassword = 'wabbalabba'
dbserver = '99.230.243.121'
dbname = 'youtubebot-dev'

# # prod database connection
# dbuser = 'postgres'
# dbpassword = 'wabbalabba'
# dbserver = '99.230.243.121'
# dbname = 'youtubebot-prod'


engine = create_engine('postgresql://%s:%s@%s:5432/%s'
                       % (dbuser, dbpassword, dbserver, dbname))
session_factory = sessionmaker(autocommit=False,
                       autoflush=False,
                       bind=engine)
Session = scoped_session(session_factory)
from TikTokApi import TikTokApi
from pathlib import Path
import os 
from tiktok.tiktok import Tiktok
from tiktok.tiktokChannel import TiktokChannel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:wabbalabba@localhost/youtubebot', echo=True)
Session = sessionmaker(bind = engine)


class TikTokHelper():


    def __init__(self):
        self.api = TikTokApi()
        self.session = Session()


    def getTrending(self, count=10):

        trending_tiktoks = self.api.trending(count=count)

        for tiktokDict in trending_tiktoks:
            nickname = tiktokDict['author']['nickname']
            channelUniqueId = tiktokDict['author']['uniqueId']
            tiktokId = tiktokDict['id']
            

            channelPath = 'data/tiktok/' + channelUniqueId
            
            if not os.path.isdir(channelPath):
                
                Path(channelPath).mkdir(exist_ok=True)
                # Add channel to database if entry doesn't exist
                q = self.session.query(TiktokChannel).filter(TiktokChannel.uniqueId == channelUniqueId).all()
                if len(q) == 0:
                    channelDict = self.api.getUser(channelUniqueId)
                    channel = TiktokChannel.channelFromChannelDict(channelDict)
                    self.session.add(channel)
                    self.session.commit()
            

            downloadLocation = channelPath + '/' + tiktokId + '.mp4'
            
            if not os.path.isfile(downloadLocation):
                # If tiktok is not downloaded, download and save in database
                vid_data = self.api.get_Video_By_TikTok(tiktokDict)
                out = open(downloadLocation, 'wb')
                out.write(vid_data)
                out.close()
                tiktok = Tiktok.tiktokFromTiktokDict(tiktokDict, downloadLocation)
                self.session.add(tiktok)


            self.session.commit()


    def getChannelTiktoks(self, channelUniqueId, count=50):

        print('Getting user {}...'.format(channelUniqueId))
        channelPath = 'data/tiktok/' + channelUniqueId

        if not os.path.isdir(channelPath):
                
                Path(channelPath).mkdir(exist_ok=True)
                # Add channel to database if entry doesn't exist
                q = self.session.query(TiktokChannel).filter(TiktokChannel.uniqueId == channelUniqueId).all()
                if len(q) == 0:
                    channelDict = self.api.getUser(channelUniqueId)
                    channel = TiktokChannel.channelFromChannelDict(channelDict)
                    self.session.add(channel)
                    self.session.commit()
                    
        tiktoks = self.api.byUsername(channelUniqueId, count=count)

        for tiktokDict in tiktoks:
            
            downloadLocation = channelPath + '/' + tiktokDict['id'] + '.mp4'     

            if not os.path.isfile(downloadLocation):
                # If tiktok is not downloaded, download and save in database
                vid_data = self.api.get_Video_By_TikTok(tiktokDict)
                out = open(downloadLocation, 'wb')
                out.write(vid_data)
                out.close()
                tiktok = Tiktok.tiktokFromTiktokDict(tiktokDict, downloadLocation)
                self.session.add(tiktok)


        self.session.commit()

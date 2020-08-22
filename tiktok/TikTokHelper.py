from TikTokApi import TikTokApi
from pathlib import Path
import os
from database.models.tiktok import Tiktok
from database.models.tiktokChannel import TiktokChannel
from database.connection import Session


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
                try:
                    channelDict = self.api.getUser(channelUniqueId)
                    channel = TiktokChannel.channelFromChannelDict(channelDict)
                    self.session.add(channel)
                    self.session.commit()
                except:
                    pass

            downloadLocation = channelPath + '/' + tiktokId + '.mp4'

            if not os.path.isfile(downloadLocation):
                # Implement logging
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
            try:
                channelDict = self.api.getUser(channelUniqueId)
                channel = TiktokChannel.channelFromChannelDict(channelDict)
                self.session.add(channel)
                self.session.commit()
            except:
                pass

        tiktoks = []

        try:
            tiktoks = self.api.byUsername(channelUniqueId, count=count)
        except Exception:
            print(Exception)

        for tiktokDict in tiktoks:
            downloadLocation = channelPath + '/' + tiktokDict['id'] + '.mp4'

            # Skip if already downloaded

            if not os.path.isfile(downloadLocation):
                vid_data = self.api.get_Video_By_TikTok(tiktokDict)
                out = open(downloadLocation, 'wb')
                out.write(vid_data)
                out.close()
                tiktok = Tiktok.tiktokFromTiktokDict(tiktokDict, downloadLocation)
                self.session.add(tiktok)
            else:
                # Log or print that tiktok is already downloaded 
                pass

        self.session.commit()

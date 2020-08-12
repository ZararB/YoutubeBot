from TikTokApi import TikTokApi
from pathlib import Path
import os 


class TikTokHelper():


    def __init__(self, dbh ):
        self.api = TikTokApi()
        #self.dbh = DbHelper('data/databases/memes.db')
        self.dbh = dbh


    def get_trending(self, count=10):
        username = tiktok 
        user_path = "data/tiktok/"+username
        Path(user_path).mkdir(parents=True, exist_ok=True)
        
        trending_tiktoks = self.api.trending(count=count)

        for tiktok in trending_tiktoks:
            

            download_location = "data/tiktok/" + username + '/' + tiktok["id"] + ".mp4"
            
            if os.path.isfile(download_location):
                print("Tiktok already Downloaded. {}".format(tiktoks_downloaded))
                tiktoks_downloaded += 1
                continue
        
            vid_data = self.api.get_Video_By_TikTok(tiktok)
            out = open(download_location, 'wb')
            out.write(vid_data)
            out.close()
            try:
                self.dbh.insert_tiktok(tiktok, download_location)
            except AttributeError as e:
                print(e)


    def get_user(self, username, count=50):
        print('Getting user {}...'.format(username))
        user_path = "data/tiktok/"+username
        Path(user_path).mkdir(parents=True, exist_ok=True)
        try:
            tiktoks = self.api.byUsername(username, count=count)
        except KeyError:
            print('KeyError')
        tiktoks_downloaded = 0 
        for tiktok in tiktoks:
            download_location = user_path + "/" + tiktok["id"] + ".mp4"
            
            # Skip if already downloaded

            if os.path.isfile(download_location):
                print("Tiktok already Downloaded. {}".format(tiktoks_downloaded))
                tiktoks_downloaded += 1
                continue

            vid_data = self.api.get_Video_By_TikTok(tiktok)
            out = open(download_location, 'wb')
            out.write(vid_data)
            out.close()
            try:
                self.dbh.insert_tiktok(tiktok, download_location)
            except AttributeError as e:
                print(e)

        

            

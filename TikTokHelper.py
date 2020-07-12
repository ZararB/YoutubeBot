from TikTokApi import TikTokApi
from DbHelper import DbHelper
from pathlib import Path
import os 
class TikTokHelper():


    def __init__(self):
        self.api = TikTokApi()
        self.dbh = DbHelper("data/databases/memes.db")
    
    def get_trending(self, count=10):

        trending_tiktoks = self.api.trending(count=count)

        for tiktok in trending_tiktoks:

            # Download Tiktok
            
            download_location = "data/tiktok/" + tiktok["id"] + ".mp4"
            tiktok_data = self.api.get_Video_By_TikTok(tiktok)
            with open(download_location, "wb") as out:
                out.write(tiktok_data)

            self.dbh.insert_tiktok(tiktok, download_location)
        pass


    def get_user(self, username, count=50):

        user_path = "data/tiktok/"+username
        Path(user_path).mkdir(parents=True, exist_ok=True)

        tiktoks = self.api.byUsername(username, count=count)

        for tiktok in tiktoks:
            download_location = user_path + "/" + tiktok["id"] + ".mp4"
            
            # Skip if already downloaded
            if os.path.isfile(download_location):
                print("Tiktok already Downloaded.")
                continue
            
            with open(download_location, "wb") as out:
                try:
                    vid_data = self.api.get_Video_By_TikTok(tiktok)
                    out.write(vid_data)
                    self.dbh.insert_tiktok(tiktok, download_location)
                except AttributeError as e:
                    print(e)

                



tkh = TikTokHelper()
tkh.get_user("charlidamelio", count=100)
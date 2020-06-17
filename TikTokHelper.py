from TikTokApi import TikTokApi
from DbHelper import DbHelper

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



tkh = TikTokHelper()

tkh.get_trending(10)

import instaloader 
from instaloader import Profile, Post
import DbHelper

class InstaHelper(object):

    def __init__(self):
        self.ldr = instaloader.Instaloader()
        self.dbh = DbHelper.DbHelper("/home/zarar/YoutubeBot2/data/memes.db")
        #self.ldr.interactive_login("memeking410")

    def download_profile(self, profile_name):
            prof = Profile.from_username(self.ldr.context, profile_name)
            posts = prof.get_posts()
            limit = 10 
            for post in posts:
                target = "/home/zarar/YoutubeBot2/data/"
                success = self.ldr.download_post(post, target )
                self.dbh.insert_post(post, target)
                limit -= 1
                if limit < 0:
                    break

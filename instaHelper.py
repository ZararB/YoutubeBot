import DbHelper 
import instaloader 
from instaloader import Post, Profile
import os


class InstaHelper(object):

    def __init__(self):
        self.ldr = instaloader.Instaloader(download_pictures=False, download_geotags=False, download_comments=False, save_metadata=False)
        self.dbh = DbHelper.DbHelper('data/databases/memes.db')

    def download_profile(self, profile_name):

        prof = Profile.from_username(self.ldr.context, profile_name)
        posts = prof.get_posts()
        os.chdir('/home/zarar/YoutubeBot2/data/meme_vids')
        for post in posts:
            target = post.mediaid
            if post.is_video & self.ldr.download_post(post, target):
                self.dbh.insert_post(post, target)

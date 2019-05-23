
from moviepy.editor import VideoFileClip, concatenate_videoclips 

import DbHelper 

class VideoNoob(object):

    def __init__(self):
        self.dbh = DbHelper.DbHelper("data/databases/memes.db")


    
    def create_video(self, num_clips=10):
        
        random_clip_locations = self.dbh.get_random_clips(num_clips)
        clips = []

        for location in random_clip_locations:
            clips.append(VideoFileClip(location))

        final_clip = concatenate_videoclips(clips)
        return final_clip.write_videofile("helloWorld.mp4")
        
        


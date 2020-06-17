
from moviepy.editor import VideoFileClip, concatenate_videoclips 
import cv2
import numpy as np
import DbHelper 

class VideoNoob(object):

    def __init__(self):
        self.dbh = DbHelper.DbHelper("data/databases/memes.db")


    
    def create_video(self, num_clips=10, height=960, width=540):
        
        random_clip_locations = self.dbh.get_random_clips(num_clips, height, width)
        clips = []

        for location in random_clip_locations:
            clips.append(VideoFileClip(location))

        final_clip = concatenate_videoclips(clips)
        
        return final_clip.write_videofile("data/videos/firstvid.mp4")
        

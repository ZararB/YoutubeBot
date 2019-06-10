
from moviepy.editor import VideoFileClip, concatenate_videoclips 
import cv2
import numpy as np
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
        
    def create_test_video(self):

        clip1 = VideoFileClip("data/meme_vids/1904396134945993987/1904396134945993987.mp4") # 480x480

        clip2 = VideoFileClip("data/meme_vids/1980541592370440887/1980541592370440887.mp4") # 480x480

        test_vid = concatenate_videoclips([clip1, clip2])
        return test_vid.write_videofile("test_vid.mp4")
        
    def video_to_clips(video_location):

        threshold = 300 

        clip_indexes = [0]
        vidcap = cv2.VideoCapture(video_location)
        l1_distances = []

        success, img1 = vidcap.read()
        success, img2 = vidcap.read()
        count = 0

        while success:
            
            l1_dist = np.abs(np.sum(img2 - img1))
            if l1_dist > threshold:
                l1_distances.append(l1_dist)
                #clip_indexes.append(count) 
            
            img1 = img2
            success, img2 = vidcap.read()
            count += 1           
             

        else:
            clip_indexes.append(count)


        return l1_distances

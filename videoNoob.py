
from moviepy.editor import *
import cv2
import numpy as np
import DbHelper 
import random 
import os
import matplotlib.pyplot as plt 

class VideoNoob(object):

        #TODO generate top10 general and top10 user 
        #TODO Incorporate views and other data into determining which vids to use  
        #TODO Should return youtubeVideo object 
        #TODO Add 'fluff' to make content more human
        #TODO Include channel names in corner along with desc, hashtags, etc 

    def __init__(self, dbh):
        self.dbh = dbh

    def create_video(self, clip_locations, vid_location, clip_dims, vid_dims=(1080, 1920, 3), template='data/backgrounds/tiktok0.png' ):
        
        clips = []

        for location in clip_locations:
            clips.append(VideoFileClip(location))
        content_clip = concatenate_videoclips(clips, method='compose')
        content_duration = content_clip.duration
        
        def make_frame(t):
            cwd = os.getcwd()
            frame = cv2.imread(template)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return rgb_frame 


        print('Making background clip...')
        background_clip = VideoClip(make_frame, duration=content_duration)
        print('Finished making background clip.')
        x = vid_dims[1]/2 - clip_dims[0]/2
        final_clip = CompositeVideoClip([background_clip, content_clip.set_position((x,0))])
        
        final_clip.write_videofile(vid_location)
        content_clip.close()
        background_clip.close()
        final_clip.close()

    def generateTikTokCompilation(self, user=None, num_clips=10, width=720,  height=1280):

        if user is not None:
            title = ''
            desc = ''
            cursor = self.dbh.conn.execute('SELECT * FROM tiktoks WHERE username = ? AND height = ? AND width = ?', (user, height, width))

            compilation_dir = 'data/videos/tiktokofficial/{}_compilations/'.format(user) 

            try:
                os.mkdir(compilation_dir)
            except FileExistsError as e:
                pass

            
            while True:
                compilationNum = len(os.listdir(compilation_dir)) + 1 
                title = "{}'s TikTok Compilation #{}".format(user, compilationNum)
                vid_location = compilation_dir + str(compilationNum) + '.mp4'
                if os.path.isfile(vid_location):
                    continue
                else:
                    break
        else:
            title = ''
            desc = ''
            cursor = self.dbh.conn.execute('SELECT * FROM tiktoks WHERE height = ? AND width = ?', (height, width))
            compilation_dir = 'data/videos/tiktokofficial/compilations/'

            try:
                os.mkdir(compilation_dir)
            except FileExistsError as e:
                pass


            while True:
                compilationNum = len(os.listdir(compilation_dir)) + 1 
                title = 'TikTok Compilation #{}'.format(compilationNum)
                vid_location = compilation_dir + str(compilationNum) + '.mp4'
                if os.path.isfile(vid_location):
                    continue
                else:
                    break
            
        tiktoks = cursor.fetchall()
        randomTikToks = random.sample(tiktoks, num_clips)

        clip_locations = [randomTikToks[i][5] for i in range(num_clips)]
        
        # Check if video was made properly
        success = self.create_video(clip_locations, vid_location, clip_dims=(width, height))

        #if success:
            #self.dbh.insertVideo(vid_location, title, desc)
            #pass

        desc = "Watch all the best TikToks on TikTok's Official Channel!"
        return (vid_location, title, desc)

    
    def generateTikTokUserCompilation(self, user):
        pass

    def generateTikTokBattle(self, user1, user2):
        pass

    def generateTopN(self, user, N):

        pass


        

        



            
         

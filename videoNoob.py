
from moviepy.editor import VideoFileClip, concatenate_videoclips 
import cv2
import numpy as np
import DbHelper 
import random 


class VideoNoob(object):

        #TODO generate top10 general and top10 user 
        #TODO Incorporate views and other data into determining which vids to use  
        #TODO Should return youtubeVideo object 
        #TODO Add 'fluff' to make content more human
        #TODO Include channel names in corner along with desc, hashtags, etc 

    def __init__(self):
        self.dbh = DbHelper.DbHelper("data/databases/memes.db")


    def create_video(self, clip_locations, vid_location):
        
        clips = []

        for location in clip_locations:
            clips.append(VideoFileClip(location))

        final_clip = concatenate_videoclips(clips)
        
        return final_clip.write_videofile(vid_location)
        

    def generateTikTokCompilation(self, user=None, num_clips=20):

        if user not None:
            title = ''
            desc = ''
            cursor = self.dbh.conn.execute('SELECT * FROM tiktoks where username = ?', (user,))
            compilation_dir = 'data/videos/tiktokofficial/{}_compilations/'
            compilationNUm = len(os.listdir(compilation_dir)) + 1 
            vid_location = compilation_dir + str(compilationNum) + '.mp4'
        
        else:
            title = ''
            desc = ''
            cursor = self.dbh.conn.execute('SELECT * FROM tiktoks')
            compilation_dir = 'data/videos/tiktokofficial/compilations/'
            compilationNUm = len(os.listdir(compilation_dir)) + 1 
            vid_location = compilation_dir + str(compilationNum) + '.mp4'

        tiktoks = cursor.fetchall()
        randomTikToks = random.sample(tiktoks, num_clips)

        clip_locations = [randomTikToks[i][5] for i in range(num_clips)]
        
        
        self.create_video(clip_locations, vid_location)


        return (vid_location, title, desc)

    
    def generateTikTokUserCompilation(self, user):
        pass

    def generateTikTokBattle(self, user1, user2):
        pass

    def generateTopN(self, user, N):

        pass


        

        



            
         

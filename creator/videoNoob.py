
from moviepy.editor import *
import cv2
import numpy as np
import random 
import os
import matplotlib.pyplot as plt 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models.tiktok import Tiktok
from database.models.tiktokChannel import TiktokChannel
from database.connection import Session

class VideoNoob(object):

        #TODO generate top10 general and top10 user 
        #TODO Incorporate views and other data into determining which vids to use  
        #TODO Should return youtubeVideo object 
        #TODO Add 'fluff' to make content more human
        #TODO Include channel names in corner along with desc, hashtags, etc 
        #TODO Rewrite using sqlalchemy 
        

    def __init__(self):
        self.session = Session()

    def createVideoFromClipLocations(self, clip_locations, vid_location, clip_dims, vid_dims=(1080, 1920, 3), template='data/backgrounds/tiktok0.png'):
        
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

    def generateTikTokCompilation(self, user=None, num_clips=10, width=576,  height=1024):

        if user is not None:
            title = ''
            desc = ''
            q = self.session.query(Tiktok).filter(Tiktok.channelUniqueId == user).filter(Tiktok.width == width).filter(Tiktok.height == height)
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
            q = self.session.query(Tiktok).filter(Tiktok.width == width).filter(Tiktok.height == height)
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
            
        tiktoks = q.all()
        num_clips = min(len(tiktoks), num_clips)
        
        if num_clips == 0:
            raise Exception
        
        randomTiktoks = random.sample(tiktoks, num_clips)

        clip_locations = [randomTiktok.fileLocation for randomTiktok in randomTiktoks]
        
        success = self.createVideoFromClipLocations(clip_locations, vid_location, clip_dims=(width, height))

        #if success:
            #self.dbh.insertVideo(vid_location, title, desc)
            #pass

        desc = "Watch all the best TikToks on TikTok's Official Channel!"
        return (vid_location, title, desc)

    

    def generateTikTokBattle(self, user1, user2, numClips=2,  width=720,  height=1280):
        
        leftClips = []
        rightClips = []
        cursor1 = self.dbh.conn.execute('SELECT * FROM tiktoks where username = ? AND height = ? AND width = ?', (user1, height, width))
        cursor2 = self.dbh.conn.execute('SELECT * FROM tiktoks where username = ? AND height = ? AND width = ?', (user2, height, width))

        user1tiktoks = cursor1.fetchall()
        user2tiktoks = cursor2.fetchall()

        for tiktok1 in user1tiktoks:
            songId1 = tiktok1[11]
            for tiktok2 in user2tiktoks:
                songId2 = tiktok2[11]

                if songId1 == songId2:
                    # Create clip of both tiktoks
                    leftClips.append(tiktok1[6])
                    rightClips.append(tiktok2[6])

            if len(leftClips) > numClips:
                break

        self.createBattleVideo(leftClips, rightClips)

        pass


    
    def createBattleVideoFromClipLocations(self, leftClips, rightClips, background='data/backgrounds/tiktok0.png'):
        clips1 = []
        clips2 = []

        for i in range(len(leftClips)):
            leftClip = VideoFileClip(leftClips[i])
            clips1.append(leftClip)
            rightClip = VideoFileClip(rightClips[i]).subclip(0, leftClip.duration)
            clips2.append(rightClip)
            

        leftClip = concatenate_videoclips(clips1, method='compose')
        rightClip = concatenate_videoclips(clips2, method='compose')
        size1 = leftClip.size
        size2 = rightClip.size
        len1 = leftClip.duration
        len2 = rightClip.duration
        leftClip.set_position(('left'))
        rightClip.set_position(('right'))

        def make_frame(t):
            cwd = os.getcwd()
            frame = cv2.imread(background)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            return rgb_frame 

        
        print('Making background clip...')
        background_clip = VideoClip(make_frame, duration=leftClip.duration)
        dur = background_clip.duration
        si = background_clip.size
        print('Finished making background clip.')

        final_clip = CompositeVideoClip([background_clip, leftClip, rightClip])
        final_clip.write_videofile('Battletest.mp4')
        leftClip.close()
        rightClip.close()
        background_clip.close()
        final_clip.close()


        return ('Battletest.mp4', 'Battle Test', 'wabba')

    def generateTopN(self, user, N):

        pass


        

        



            
         

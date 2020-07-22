
from moviepy.editor import VideoFileClip, concatenate_videoclips 
import cv2
import numpy as np
import DbHelper 
import random 


class VideoNoob(object):

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



        pass
    
    def generateTikTokUserCompilation(self, user):
        pass

    def generateTikTokBattle(self, user1, user2):
        pass

    def generateTopN(self, user, N):

        pass


    def generateTikTokVideo(self, users, TYPE='compilation', num_clips=2):
        
        #TODO generate top10 general and top10 user 
        #TODO Incorporate views and other data into determining which vids to use  
        #TODO Should return youtubeVideo object 
        #TODO Divide into multiple functions? 
        #TODO Add 'fluff' to make content more human
        #TODO Include channel names in corner along with desc, hashtags, etc 
        


        if TYPE == 'compilation':
            compilationNumber = random.randint(1, 30)
            
            title = 'Best TikToks Compilation # ' + str(compilationNumber)
            desc = 'Watch all the best TikToks in one place.'
            cursor = self.dbh.conn.execute('SELECT * FROM tiktoks')
            tiktoks = cursor.fetchall()
            randomTikToks = random.sample(tiktoks, num_clips)

            clip_locations = [randomTikToks[i][5] for i in range(num_clips)]
            vid_location = 'data/videos/tiktokofficial/randomCompilation' + str(compilationNum) + '.mp4'
            
            self.create_video(clip_locations, vid_location)

            return (vid_location, title, desc)



        elif TYPE == 'userCompilation':
            if len(users) != 1:
                print('Cannot generate video. Incorrect number of users.')
                #TODO Raise exception instead of returning None
                return None
            compilationNumber = random.randint(1, 30)
            title = "{}'s Best TikToks Compilation # ".format(users[0]) + str(compilationNumber)
            
            desc = 'Watch all the best TikToks in one place.'

            cursor = self.dbh.conn.execute('SELECT * FROM tiktoks where username = ?', (users[0],))
            tiktoks = cursor.fetchall()
            randomTikToks = random.sample(tiktoks, num_clips)

            clip_locations = [randomTikToks[i][5] for i in range(num_clips)]
            vid_location = 'data/videos/tiktokofficial/' + users[0] + '_' + str(compilationNumber) + '.mp4'

            self.create_video(clip_locations,vid_location)

            return (vid_location, title, desc)


            
         

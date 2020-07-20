
from moviepy.editor import VideoFileClip, concatenate_videoclips 
import cv2
import numpy as np
import DbHelper 
import random 


class VideoNoob(object):

    def __init__(self):
        self.dbh = DbHelper.DbHelper("data/databases/memes.db")


    def create_video(self, clip_locations):
        
        clips = []

        for location in clip_locations:
            clips.append(VideoFileClip(location))

        final_clip = concatenate_videoclips(clips)
        
        return final_clip.write_videofile("data/videos/firstvid.mp4")
        


    def generateTikTokVideo(self, users, TYPE='compilation', num_clips=2):

        #TODO Should return youtubeVideo object 

        if TYPE == 'compilation':
            title = 'Best TikToks Compilation # ' + str(random.randint(1,30))
            desc = 'Watch all the best TikToks in one place.'
            cursor = self.dbh.conn.execute('SELECT * FROM tiktoks')
            tiktoks = cursor.fetchall()
            randomTikToks = random.sample(tiktoks, num_clips)

            clip_locations = [randomTikToks[i][5] for i in range(num_clips)]
            vid_location = self.create_video(clip_locations)

            return (vid_location, title, desc)



        elif TYPE == 'userCompilation':
            if len(users) != 1:
                print('Cannot generate video. Incorrect number of users.')
                return None

            title = "{}'s Best TikToks Compilation # ".format(users[0]) + str(random.randint(1,30))
            desc = 'Watch all the best TikToks in one place.'

            cursor = self.dbh.conn.execute('SELECT * FROM tiktoks where username = ?', (users[0],))
            tiktoks = cursor.fetchall()
            randomTikToks = random.sample(tiktoks, num_clips)

            clip_locations = [randomTikToks[i][5] for i in range(num_clips)]
            vid_location = self.create_video(clip_locations)

            return (vid_location, title, desc)


            
         

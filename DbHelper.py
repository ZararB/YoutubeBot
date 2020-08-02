import sqlite3 as sql 
import numpy as np 
import random
import cv2
import subprocess
from subprocess import PIPE, STDOUT
from moviepy.editor import VideoFileClip
import TikTokApi as tiktokapi
import os
#TODO Rewrite using SQLAlchemy 
#TODO Create YoutubeChannels table (id, channel_name, subs, total_view, tags ex. tiktok, sports, fortnite etc, num_vids ....)
#TODO Write Function to populate YoutubeChannels table 
#TODO Clean tiktok database by removing tiktoks that dont meet certain criteria set by other tiktoks (ex average num_views)
#TODO Add numTimesUsed column and averageVidViews column in tiktok table to improve quality of database over time 



class DbHelper(object):
    

    def __init__(self, db_dir):
        

        CREATE_TABLES_SQL = '''
        
        
        CREATE TABLE IF NOT EXISTS clips(
            id integer primary key,
            media_id integer,
            file_location string, 
            source_platform string,
            duration integer,
            width integer,
            height integer,
            desc string
        );

        CREATE TABLE IF NOT EXISTS tiktoks(
            id integer primary key,
            tiktok_id integer,
            username string,
            desc string, 
            play_count integer,
            download_addr string,
            file_location string,
            duration integer,
            width integer,
            height integer,
            song_name string,
            song_id integer
        );

        CREATE TABLE IF NOT EXISTS videos(
            id integer primary key, 
            media_id integer,
            channel string,
            file_location string,
            thumbnail_location string,
            title string,
            desc string, 
            duration integer,
            upload_date integer,
            views integer
        );

        CREATE TABLE IF NOT EXISTS my_videos(
            id integer primary key,
            channel string,
            file_location string,
            thumbnail_location string,
            upload_date integer,
            views integer
        );

        CREATE TABLE IF NOT EXISTS tiktok_channels(
            id integer primary key,
            nickname string,
            uniqueId string
        )
        '''
        
        # Additional tables to add later

        self.conn = sql.connect(db_dir)
        cursor = self.conn.cursor()
        cursor.executescript(CREATE_TABLES_SQL)


    def insert_tiktok(self, tiktok, download_location):

        _id = int(tiktok["id"])
        username = tiktok['author']['uniqueId']
        desc = tiktok['desc']
        play_count = tiktok['stats']['playCount']
        download_addr = tiktok['video']['downloadAddr']
        duration = tiktok["video"]["duration"]
        width = tiktok["video"]["width"]
        height = tiktok["video"]["height"]
        desc = tiktok["desc"]
        source_platform = "tiktok"
        song_name = tiktok['music']['title']
        if tiktok['music']['id'] != '':
            song_id = int(tiktok['music']['id'])

        else:
            song_id = -1

        insert_tiktok_sql = '''insert into tiktoks(tiktok_id, username, desc, play_count, download_addr ,file_location, duration, width, height, song_name, song_id) values (?,?,?,?,?,?,?,?,?,?,?)'''
        cursor = self.conn.cursor()
        cursor.execute(insert_tiktok_sql, (_id, username, desc, play_count, download_addr, download_location, duration, width, height, song_name, song_id))
        self.conn.commit()


    def insert_post(self, post, target):

        media_id = post.mediaid
        file_location = 'data/meme_clips/' + str(target) + "/" +  str(target) + ".mp4"
        duration = post.video_duration
        insert_post_sql = '''insert into clips(media_id, file_location, duration, height, width) values (?,?,?,?,?)'''
        
        # Finds the dimensions of the video using cv2
        vid = cv2.VideoCapture(file_location)
        height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        cursor = self.conn.cursor()
        cursor.execute(insert_post_sql, (media_id, file_location, duration, height, width))
        self.conn.commit()
        

    def get_random_clips(self, num_clips, height, width):
            
        # An array with the dir of random clips  
        clip_locations = [] 

        # Query the entire instagram_clips table 
        cursor = self.conn.cursor()
        query = cursor.execute("select file_location from clips where height = ? and width = ?", (height, width))
        rows = query.fetchall()
        total_count = len(rows)

        # Determine the indices of the random clips
        clip_indices = random.sample(range(total_count), num_clips)

        for idx in clip_indices:
            clip_locations.append(rows[idx][0])

        return clip_locations


    def update(self):
        """ 
        Checks the database for entries that have not been downloaded 
        and downloads them. 
        Deletes duplicates. 
        """

        cursor = self.conn.cursor()
        full_query = cursor.execute("select * from instagram_clips")
        field_names = [i[0] for i in cursor.description]

        # Determine column indices for each parameter
        height_col_index = field_names.index("height")
        width_col_index = field_names.index("width")
        duration_col_index = field_names.index("duration")
        file_location_index = field_names.index("file_location")
        media_id_index = field_names.index("media_id")

        rows = full_query.fetchall()

        for row in rows:
            # 
            id = row[0]
            media_id = row[media_id_index] 
            file_location = row[file_location_index]
            height = row[height_col_index]
            width = row[width_col_index]
            duration = row[duration_col_index]

            # If video dimensions are missing, determine them using cv2 and update database
            if height is None or height == 0:
                
                vid = cv2.VideoCapture(file_location)
                height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
                width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)

                cursor.execute("UPDATE instagram_clips SET width = ?, height = ? WHERE media_id = ?",
                    (width, height, media_id))
    
            # If video duration is missing, use moviepy to determine it and update the database
            if duration is None or duration == 0:
                
                clip = VideoFileClip(file_location)
                clip_duration = clip.duration
                clip.close()

                cursor.execute("UPDATE instagram_clips SET duration = ? WHERE media_id = ?",
                    (clip_duration, media_id))

                print(id, clip_duration)


            self.conn.commit()
        

    def insert_video(self, vid_location, title, desc):


            
        pass 

        
    def update0(self):
        '''
        Loops through every table and fills in missing data and downloads files that are missing
        '''

        cursor = self.conn.execute('SELECT * FROM tiktoks') 
        tiktoks = cursor.fetchall()

        for tiktok in tiktoks:

            # Download if not downloaded
            file_location = tiktok[6]
            download_addr = tiktok[5]
            if os.path.isfile(file_location):
                continue
            else:
                tiktokapi.get_Video_By_DownloadURL(download_addr)

        

        tikTokRootDir = os.getcwd() + '/tiktok/'
        downloadedTikTokFiles = []
        for path, subdirs, files in os.walk(tikTokRootDir):

            for name in files:
                fileLocation = os.path.join(path, name)
                titkok_db_search = self.conn.cursor('select * from tiktoks where file_location = ?', fileLocation)

                if len(tiktok_db_search.fetch_all()) != 1:
                    tiktokId = fileLocation.split('/')[-1][:-4]

                    tiktok = tiktokapi.getTikTokById(tiktokId)
                    self.insert_tiktok(tiktok, fileLocation)
                    downloadedTikTokFiles.append(os.path.join(path, name))

                else:
                    print('Tiktok already in Database')

                

       


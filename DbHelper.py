import sqlite3 as sql 
from instaloader import Post
import numpy as np 
import random
import subprocess
from subprocess import PIPE, STDOUT


class DbHelper(object):


    def __init__(self, db_dir):
        

        CREATE_TABLES_SQL = '''CREATE TABLE IF NOT EXISTS meme_clips (
            id integer primary key,
            source text,
            ref_id integer default -1,
            file_location text default "" , 
            length integer default -1, 
            width integer default -1,
            height integer default -1
            );'''
            # Additional tables to add later

        self.conn = sql.connect(db_dir)
        cursor = self.conn.cursor()
        cursor.executescript(CREATE_TABLES_SQL)

    def insert_post(self, post, target):

        ref_id = post.mediaid
        file_location = 'data/meme_clips/' + str(target) + "/" +  str(target) + ".mp4"
        length = post.video_duration
        insert_post_sql = '''insert into meme_clips(source, ref_id, file_location, length) values (?,?,?,?)'''
        
        cursor = self.conn.cursor()
        cursor.execute(insert_post_sql, ("instagram", ref_id, file_location, length))
        self.conn.commit()
        

    def get_random_clips(self, num_clips):
            
        # An array with the dir of random clips 
        clip_locations = []
        cursor = self.conn.execute("select count(*) from meme_clips")
        total_count = cursor.fetchone()[0]
        clip_ids = random.sample(range(total_count), num_clips)

        for id in clip_ids:
            row = self.conn.execute("select * from meme_clips where id = ?;", ((id, )))
            clip = row.fetchone()
            if clip != None:
                clip_locations.append(clip[2]+"/"+str(clip[1])+".mp4")

        return clip_locations


    def update(self):
        """ 
        Checks the database for entries that have not been downloaded 
        and downloads them. 
        Deletes duplicates. 
        """

        # Loops through the entire dataset

        cursor = self.conn.cursor()
        full_query = cursor.execute("select * from meme_clips")
        field_names = [i[0] for i in cursor.description]

        height_col_index = field_names.index("height")
        width_col_index = field_names.index("width")
        file_location_index = field_names.index("file_location")
        ref_id_index = field_names.index("ref_id")

        rows = full_query.fetchall()

        for row in rows:
            id = row[0]
            ref_id = row[ref_id_index] 
            file_location = row[file_location_index]
            height = row[height_col_index]
            width = row[width_col_index]

            # If video dimensions are missing, find them using ffmpeg and update the row
            if height == -1 or width == -1:

                
                out = subprocess.run(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', file_location])
                type(out)

                cursor.execute("UPDATE meme_clips SET width = ?, height = ? WHERE id = ?", (int(width), int(height), id))
                
        self.conn.commit()
        



dbh = DbHelper("data/databases/memes.db")

dbh.update()


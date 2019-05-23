import sqlite3 as sql 
from instaloader import Post
import numpy as np 
import random



class DbHelper(object):


    def __init__(self, db_dir):
        """ Creates memes database with meme_vids table with columns (
            id, media_id, file_location, length, likes, owner_id, owner_follower_count
            )
            """
        CREATE_TABLES_SQL = '''CREATE TABLE IF NOT EXISTS meme_vids (
            id integer primary key,
            media_id integer, 
            file_location text, 
            length integer, 
            num_likes integer, 
            owner_id integer, 
            owner_follower_count integer);
            '''

        self.conn = sql.connect(db_dir)
        cursor = self.conn.cursor()
        cursor.execute(CREATE_TABLES_SQL)

    def insert_post(self, post, target):

        media_id = post.mediaid
        file_location = 'data/meme_vids/' + str(target)
        length = post.video_duration
        num_likes = post.likes
        owner_id = post.owner_id
        owner_follower_count = post.owner_profile.followers

        insert_post_sql = '''insert into meme_vids(media_id, file_location, length, num_likes,
        owner_id, owner_follower_count) values(?,?,?,?,?,?) '''
        cursor = self.conn.cursor()
        cursor.execute(insert_post_sql, (media_id, file_location, length, num_likes, owner_id, owner_follower_count))
        self.conn.commit()
        

    def get_random_clips(self, num_clips):
            
        # An array with the dir of random clips 
        clip_locations = []
        cursor = self.conn.execute("select count(*) from meme_vids")
        total_count = cursor.fetchone()[0]
        clip_ids = random.sample(range(total_count), num_clips)

        for id in clip_ids:
            row = self.conn.execute("select * from meme_vids where id = ?;", ((id, )))
            clip = row.fetchone()
            if clip != None:
                clip_locations.append(clip[2]+str(clip[1])+".mp4")

        return clip_locations

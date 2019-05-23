import DbHelper
import sqlite3 as sql

dbh = DbHelper.DbHelper("data/databases/memes.db")

locations = dbh.get_random_clips()
print(locations)
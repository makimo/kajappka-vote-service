import os

from pymongo import MongoClient


client = MongoClient(os.environ['DATABASE_URI'])
db = client['votes']
votes_coll = db.votes

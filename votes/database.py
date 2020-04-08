import os

from pymongo import MongoClient


client = MongoClient(os.environ['DATABASE_URI'])
db = client[os.environ['DATABASE']]
votes_coll = db.votes

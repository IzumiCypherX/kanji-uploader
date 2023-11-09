from .config import *

from telegram.ext import Application
from pymongo import MongoClient

client = MongoClient(MONGO_URI)
db = client['kanjiupload']
collection = db.get_collection('kanji')

app = Application.builder().token(TOKEN).build()
from .config import *

from telegram.ext import Application
from pymongo import MongoClient

import logging

client = MongoClient(MONGO_URI)
db = client['kanjiupload']
collection = db.get_collection('kanji')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

logging.getLogger('httpx').setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

app = Application.builder().token(TOKEN).build()
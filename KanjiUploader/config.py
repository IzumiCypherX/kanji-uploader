import os
import dotenv

dotenv.load_dotenv("config.env")

KANJI_API = os.environ.get("KANJI_API")
API_KEY = os.environ.get("API_KEY")
TOKEN = os.environ.get("TOKEN")

DELAY = int(os.environ.get("delay"))

MONGO_URI = os.environ.get("MONGO_URI")
CHANNEL_ID = int(os.environ.get("CHANNEL_ID"))
LOG_ID = int(os.environ.get("LOG_ID"))
OWNER_ID = int(os.environ.get("OWNER_ID"))
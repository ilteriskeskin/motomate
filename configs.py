import os

from dotenv import load_dotenv

load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

SECRET_KEY = os.getenv("SECRET_KEY")

GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
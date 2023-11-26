import os
from dotenv import load_dotenv
from json import loads
load_dotenv()

GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
HOST = os.environ["HOSTNAME_URI"]
FIREBASE_CERT = loads(os.environ["FIREBASE_SERVICE_ACC"])
FIREBASE_CONFIG = loads(os.environ["FIREBASE_CONFIG"])

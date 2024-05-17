import os
import firebase_admin
import firebase
from dotenv import load_dotenv
from json import loads
from firebase_admin import credentials, firestore

# load environment variables
load_dotenv()

GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
HOST = os.environ["HOSTNAME_URL"]
FIREBASE_CERT = loads(os.environ["FIREBASE_SERVICE_ACCOUNT"])
FIREBASE_CONFIG = loads(os.environ["FIREBASE_CONFIG"])
COOKIE_NAME = os.environ["SESSION_COOKIE_NAME"]

# initialize firebase admin sdk
_cred = credentials.Certificate(FIREBASE_CERT)
_fir_app = firebase_admin.initialize_app(_cred)
# initialize firestore client
db = firestore.client()

# initialize firebase auth
_firebase_app = firebase.initialize_app(FIREBASE_CONFIG)
web_auth = _firebase_app.auth()

POSTGRES_USER = os.environ["POSTGRES_USER"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_DB = os.environ["POSTGRES_DB"]
POSTGRES_HOST = os.environ["POSTGRES_HOST"]

FIRESTORE_COLLECTION = os.environ["FIRESTORE_COLLECTION"]

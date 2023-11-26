import os
import firebase_admin
import firebase
from dotenv import load_dotenv
from json import loads
from firebase_admin import credentials, firestore
load_dotenv()

GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
HOST = os.environ["HOSTNAME_URI"]
FIREBASE_CERT = loads(os.environ["FIREBASE_SERVICE_ACC"])
FIREBASE_CONFIG = loads(os.environ["FIREBASE_CONFIG"])

_cred = credentials.Certificate(FIREBASE_CERT)
_fir_app = firebase_admin.initialize_app(_cred)
db = firestore.client()

_firebase_app = firebase.initialize_app(FIREBASE_CONFIG)
web_auth = _firebase_app.auth()

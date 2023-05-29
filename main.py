from __future__ import division
from fastapi import FastAPI, Depends, Request, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import firebase_admin
from firebase_admin import credentials, firestore
import os, typing
from api_globals import GlobalsMiddleware, g
import pandas as pd
from qrcode.image.pil import PilImage

cred = credentials.Certificate('aventus-website.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

firebaseConfig = {
  'apiKey': "AIzaSyDIerahYw7xS6madhWGYuvF2n8A3-VMUkg",
  'authDomain': "aventus-b0068.firebaseapp.com",
  'databaseURL': "https://aventus-b0068-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "aventus-b0068",
  'storageBucket': "aventus-b0068.appspot.com",
  'messagingSenderId': "1004778993565",
  'appId': "1:1004778993565:web:5ccb91f7a09dede0342174",
  'measurementId': "G-LEE5266T98"
}

app = FastAPI()
router = APIRouter()

app.add_middleware(GlobalsMiddleware)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")



def flash(request: Request, message: typing.Any, category: str = "primary") -> None:
   if "_messages" not in request.session:
       request.session["_messages"] = []
       request.session["_messages"].append({"message": message, "category": category})

def get_flashed_messages(request: Request):
   print(request.session)
   return request.session.pop("_messages") if "_messages" in request.session else []

templates.env.globals['get_flashed_messages'] = get_flashed_messages

@app.on_event("startup")
async def load_data():
    g.df = pd.read_csv('teams.csv')

@app.get("/", dependencies=[Depends(load_data)], response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/barcode_reader", response_class=HTMLResponse)
async def barcode_reader(request: Request):
    return templates.TemplateResponse('barcode_reader_page.html', {"request": request})

@app.get("/scan_qr/", dependencies=[Depends(load_data)])
async def add_entry(uid: str):
    s = uid in g.df['UID'].tolist()
    if s:
        details = g.df.loc[g.df['UID'] == uid].values
        print(details[0].tolist())
        return {'Team Member': 'Found', 'Details': details[0].tolist()}
    else:
        return {'Team Member': 'NOT Found'}
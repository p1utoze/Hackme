from __future__ import division
from fastapi import FastAPI, Depends, Request, APIRouter, L
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware

import firebase_admin
from firebase_admin import credentials, firestore
import os, typing
from api_globals import GlobalsMiddleware, g
import pandas as pd
from qrcode.image.pil import PilImage
from json import loads

cred = credentials.Certificate('aventus-website.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

__admin_users =

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

allow_all = [*]
app.add_middleware(GlobalsMiddleware)
app.add_middleware(
   CORSMiddleware,
   allow_origins=allow_all,
   allow_credentials=True,
   allow_methods=allow_all,
   allow_headers=allow_all
)
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
    # return templates.TemplateResponse("home.html", {"request": request})
    return RedirectResponse("https://hackaventus.com/")


@app.get("/barcode_reader", response_class=HTMLResponse)
async def barcode_reader(request: Request):
    return templates.TemplateResponse('barcode_reader_page.html', {"request": request})

@app.get("/register/", dependencies=[Depends(load_data)])
async def add_entry(uid: str):
    s = uid in g.df['UID'].tolist()
    if s:
        details = loads(g.df.loc[g.df['UID'] == uid].to_json(orient='records'))
        return {'Team Member': 'Found', 'Details': details[0]}
    else:
        return {'Team Member': 'NOT Found'}

@app.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.post("/login/")
async def login(request: Request, db: Session = Depends(get_db)):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("auth/login.html", form.__dict__)
            login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("auth/login.html", form.__dict__)
    return templates.TemplateResponse("auth/login.html", form.__dict__)
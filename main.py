from __future__ import division
from fastapi import FastAPI, Depends, Request, APIRouter, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from pydantic import BaseModel
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.base_query import FieldFilter
# import os, typing
from api_globals import GlobalsMiddleware, g
import pandas as pd
from json import loads
import time
from routers.login_form import LoginForm

import firebase
import requests
# import pyrebase
from routers.login_form import LoginForm
from fastapi.responses import JSONResponse



cred = credentials.Certificate('aventusauth.json')
firebase_admin.initialize_app(cred)

db = firestore.client()
# firebaseConfig = {
#   "apiKey": "AIzaSyBgT68Ra8QzLU6WkSgFTX0ws2Veupng7EE",
#   "authDomain": "test-aventus.firebaseapp.com",
#   "projectId": "test-aventus",
#   "storageBucket": "test-aventus.appspot.com",
#   "messagingSenderId": "330950556473",
#   "appId": "1:330950556473:web:03f5b5c3071c20a56546e8",
#   "measurementId": "G-0JVRVC3R7K"
# };
# firebaseConfig = {
#   "apiKey": "AIzaSyBq2PUePkbjGHpYr8LxycuUIOIri-9KjTQ",
#   "authDomain": "aventusauth.firebaseapp.com",
#   "projectId": "aventusauth",
#   "storageBucket": "aventusauth.appspot.com",
#   "messagingSenderId": "629066554537",
#   "appId": "1:629066554537:web:3c9ab2209d641e9f1bddb8",
#   "measurementId": "G-CBDJE2FYYZ",
#   "databaseURL": ""
# }
firebaseConfig = {
  "apiKey": "AIzaSyBq2PUePkbjGHpYr8LxycuUIOIri-9KjTQ",
  "authDomain": "aventusauth.firebaseapp.com",
  "databaseURL": "https://aventusauth-default-rtdb.firebaseio.com",
  "projectId": "aventusauth",
  "storageBucket": "aventusauth.appspot.com",
  "messagingSenderId": "629066554537",
  "appId": "1:629066554537:web:95d99df7082809151bddb8",
  "measurementId": "G-FXSXEHPRSR"
};

firebase_app = firebase.initialize_app(firebaseConfig)
auth = firebase_app.auth()

app = FastAPI()
api_router = APIRouter()
# api_router.include_router(login.router, prefix="", tags=["auth-webapp"])

allow_all = ['*']
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

class LoginCredentials(BaseModel):
    email: str
    password: str

      
def check_participant(uid=None, is_admin=None):
    if not uid:
        # SEND PAYLOAD FOR RENDERING list_teams.html
        return "NULL UID"
    return "UID exists"
    uid = uid.strip()

    print(f'"{uid}"')
    # Registered participants
    s = uid in g.df['UID'].tolist()
    if s:
        participants = "participants"
        cursor = db.collection(participants)
        query = cursor.where(filter=FieldFilter("UID", "==", uid)).get()

        try:
            data = query[0].to_dict()
            print(f'{query[0].id} => {data}')
        except IndexError:
            data = {}
            print("No data found")

        # Check if uid in firestore
        if data:
            print("Rendering checkin_checkout page...")
            status = "NOT CHECKED"
            # return status, {'UID': uid}
            if request.cookies.get('firebase_token'):
                pass
                # return templates.TemplateResponse(
                # 'checkin_out.html', {'request': request, 'UID': uid, 'password': "aventus@6969", "status": status})
            # return templates.TemplateResponse(
            #                 'checkin_out.html', {'request': request, 'UID': uid, 'password': "aventus@6969", "status": status})

        details = g.df.loc[g.df['UID'] == uid].to_json(orient='records')
        doc = loads(details[1:-1])
        doc['status'] = "NULL"
        member_status = "UNREGISTERED"
        # payload = {'request': request, 'Team Member': member_status, 'Details': doc}
        print(doc)
        # db.collection(participants).document(uid).set(doc)
        # return templates.TemplateResponse('master_checkin.html', payload)
        
    else:
        # Invalid
        return "INVALID UID", {'Error': 'INVALID UID FOUND'},

@app.on_event("startup")
async def load_data():
    g.df = pd.read_csv('teams.csv')


@app.get("/")
async def home(request: Request, uid: str = None):
    # return templates.TemplateResponse("status_result.html", {"request": request})
    firebase_user_id = request.cookies.get('firebase_token')
    if not firebase_user_id:
        return templates.TemplateResponse("login.html", {"request": request})
        # return {"THUS": "THIS"}
    out = check_participant(uid)
    # output = check_participant(uid=uid)
    return {"OUTPUT" : out, "UID": uid}
    #

@app.post("/")
async def kuchbhi(response: LoginCredentials, uid: str = None):
    # HANDLE FOR INCORRECT LOGIN CREDENTIAL
    user = auth.sign_in_with_email_and_password(response.email, response.password)

    response = JSONResponse(content={})
    response.set_cookie(key="firebase_token", value=user['idToken'], secure=True, httponly=True, samesite='none')
    output = check_participant(uid=uid)
    return {'output': output}


@app.get("/demo/")
async def scan_route(request: Request):
    firebase_user_id = request.cookies.get('firebase_token')
    print(firebase_user_id)
    return {"message": f"Scan route accessed by user: {firebase_user_id}"}



@app.get("/qr_scan/", dependencies=[Depends(load_data)], response_class=HTMLResponse)
async def add_entry(request: Request, uid: str):
    member_status = check_participant(uid)

    return templates.TemplateResponse("login.html", {"request": request})



@app.post("/checkin_out/{uid}")
async def checkin_out(request: Request, uid: str):
    # print(uid)
    # now = datetime.now()
    # entry_time = now.strftime("%d/%m/%Y %H:%M:%S ")
    entry_time = time.strftime("%d/%m/%Y %I:%M:%S %p", time.gmtime(time.time() + 19800))
    participants = "participants"
    cursor = db.collection(participants)
    query = cursor.where(filter=FieldFilter("UID", "==", uid)).get()
    data = query[0].to_dict()
    status_val = None
    try:
        if data['status'] == "NULL":
            print("Added status entry: IN")
            status_val = "IN"
            cursor.document(uid).update({'status': "IN"})
            cursor.document(uid).update({'checkin': firestore.ArrayUnion([entry_time])})
        elif data['status'] == "IN":
            print("Added status entry: OUT")
            status_val = "OUT"
            cursor.document(uid).update({'status': "OUT"})
            cursor.document(uid).update({'checkout': firestore.ArrayUnion([entry_time])})
        elif data['status'] == 'OUT':
            print("Added status entry: IN")
            status_val = "IN"
            cursor.document(uid).update({'status': "IN"})
            cursor.document(uid).update({'checkin': firestore.ArrayUnion([entry_time])})
    except:
        print("wrong status")
    finally:
        # payload = {'request': Request, "details": data, "status_value": status_val, "status": "CHECKED"}
        return {"API": "WORKS"}

    # return {"API": "called successfully"}
    # except:
    #     print("ERROR")
    #     return {"Internal Error": "Problem in the code"}

@app.post("/register")
async def register(track: str= Form(), team_id:str= Form()):
    team_members=[]
    doc=db.collection('participants')
    query = doc.where(filter=FieldFilter('teamCode', "==", "AIML01")).stream()
    try:
        print(query)
        for d in query:
            print(f'{d.id} => {d.to_dict()}')
    except IndexError:
        data = {}
        print("No data found")
    # team_name=data
    # print(data, team_name)

    # db.collection(participants).document(uid).set(doc)
    return {"API": 'WORKING'}




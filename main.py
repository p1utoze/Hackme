import gunicorn.app.wsgiapp
import uvicorn
from fastapi import FastAPI, Depends, Request, APIRouter, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
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

import firebase
import requests
# import pyrebase
from fastapi.responses import Response, RedirectResponse, JSONResponse, HTMLResponse


cred = credentials.Certificate('aventusauth.json')
fir_app = firebase_admin.initialize_app(cred)
db = firestore.client()
firebaseConfig = {
  "apiKey": "AIzaSyDYt2Mj95NipbFOhBMb3jDsdUoXi7YFFUc",
  "authDomain": "hackme-60c66.firebaseapp.com",
  "databaseURL": "https://hackme-60c66-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "hackme-60c66",
  "storageBucket": "hackme-60c66.appspot.com",
  "messagingSenderId": "505276403628",
  "appId": "1:505276403628:web:4e292a5a0395c348543409",
  "measurementId": "G-QR40ZRVFT3"
};
#
firebase_app = firebase.initialize_app(firebaseConfig)
auth = firebase_app.auth()

app = FastAPI()
api_router = APIRouter()

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
        return 602
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
            print("ALREADY REGISTERED USER. REDIRECTING TO CHECKIN...")
            return 600
        print("NOT REGISTERED. REDIRECTING TO REGISTRATION...")
        return 601
            # return status, {'UID': uid}

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
    g.df = pd.read_csv('Final_List.csv')

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, uid: str = None):
    firebase_user_id = request.cookies.get('firebase_token')
    if firebase_user_id:
        return templates.TemplateResponse("update.html", {"request": request})
        # return {"THUS": "THIS"}
    # out = check_participant(uid)
    # output = check_participant(uid=uid)
    # return {"OUTPUT": "Bruh", "UID": uid}
    return templates.TemplateResponse("login.html", {"request": request})


# @app.post("/")
# async def kuchbhi(response: LoginCredentials, uid: str = None):
#     # HANDLE FOR INCORRECT LOGIN CREDENTIAL
#     user = auth.sign_in_with_email_and_password(response.email, response.password)
#     print(user)
#     responsess = JSONResponse(content={})
#     responsess.set_cookie(key="firebase_token", value=user['idToken'], secure=True, httponly=True, samesite='none')
#     # output = check_participant(uid=uid)
#     return {'output': 'helloworld'}

@app.post("/", response_class=HTMLResponse)
async def kuchbhi(response: Response, email: str = Form(), password: str = Form(), uid: str = None, ):
    # HANDLE FOR INCORRECT LOGIN CREDENTIAL
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(user)
        # response = JSONResponse(content={})
        # response.status_code = 200
        response.set_cookie(key="firebase_token", value=user['idToken'], secure=True, httponly=True, samesite='none')
        base_url = "https://aventus-hackaventus.b4a.run/"
        # print(response.body)
        # return "/regis"
        return f"""
            <html>
            <head>
                <title>Login</title>
                <meta http-equiv = "refresh" content = "3; url = { base_url }" 
            </head>
            <body>
                <h1 style="color:green">Login Successful!</h1>
                <br>
                <h3>Please refresh the page again or go to previous page</h3>
            </body>
            </html>
            """
        # return templates.TemplateResponse("update.html", {"request": request})
    except requests.exceptions.HTTPError as e:
        err_message = loads(e.strerror)['error']['message']
        print("THIS ERROR", err_message)
        return f'''
        <html>
            <head>
                <title>Login</title>
            </head>
            <body>
                <h1 style="color:red">Login Failed!</h1>
                <br>
                <h3>{err_message}</h3>
                <br><br>
                <h4><i>Refresh again or go to previous page</i></h4>
            </body>
            </html>'''
        # return templates.TemplateResponse("login.html", {"request": request, 'error': err_message})
    # output = check_participant(uid=uid)
    # return {'output': output}


@app.get("/demo/")
async def scan_route(request: Request):
    firebase_user_id = request.cookies.get('firebase_token')
    print("SEXY", firebase_user_id)
    return {"BLA": "BAA"}
    # print(help(RedirectResponse))
    # return {"message": f"Scan route accessed by user: {firebase_user_id}"}


@app.get("/qr_scan/", dependencies=[Depends(load_data)], response_class=HTMLResponse)
async def add_entry(request: Request, uid: str):
    if not request.cookies.get('firebase_token'):
        base_url = "https://aventus-hackaventus.b4a.run/"
        return templates.TemplateResponse('login.html', {"request": request, "redirect": True, "base_url": base_url})
    member_status_code = check_participant(uid)
    if member_status_code == 600:
        entry_time = time.strftime("%d/%m/%Y %I:%M:%S %p", time.gmtime(time.time() + 19800))
        participants = "participants"
        cursor = db.collection(participants)
        query = cursor.where(filter=FieldFilter("UID", "==", uid)).get()
        data = query[0].to_dict()
        status_val = None
        try:
            if data['status'] == "NULL":
                print("Added status entry: IN")
                cursor.document(uid).update({'status': "IN"})
                cursor.document(uid).update({'checkin': firestore.ArrayUnion([entry_time])})
            elif data['status'] == "IN":
                print("Added status entry: OUT")
                cursor.document(uid).update({'status': "OUT"})
                cursor.document(uid).update({'checkout': firestore.ArrayUnion([entry_time])})
            elif data['status'] == 'OUT':
                print("Added status entry: IN")
                cursor.document(uid).update({'status': "IN"})
                cursor.document(uid).update({'checkin': firestore.ArrayUnion([entry_time])})
        except:
            print("wrong status")
        finally:
            # payload = {'request': Request, "details": data, "status_value": status_val, "status": "CHECKED"}
            return templates.TemplateResponse("status_result.html",
                                              {"request": request,
                                               "status": data['status'],
                                               "fname": data['firstName'],
                                               "lname": data['lastName']})
    elif member_status_code == 601:
        details = g.df.loc[g.df['UID'] == uid].to_json(orient='records')
        doc = loads(details[1:-1])
        doc['status'] = "NULL"

        return templates.TemplateResponse('master_checkin.html', {"request": request, "Details": doc})






@app.post("/status", response_class=HTMLResponse)
async def register(request: Request, track: str = Form(), team_id: str = Form()):
    member_ids=[]
    member_names = []
    all_timings = []
    status_list = []
    team_name = None
    doc = db.collection('participants')
    query = doc.where(filter=FieldFilter('teamCode', "==", team_id)).stream()
    try:
        # print(query)
        for d in query:
            # print(d.__dict__)
            details = d.to_dict()
            # print(details)
            member_ids.append(details['UID'])
            member_names.append(" ".join([details['firstName'], details['lastName']]))
            if not team_name:
                team_name = details['teamName']
            all_timings.append({'IN': details.get('checkin', " "), "OUT": details.get('checkout', "")})
            status_list.append(details['status'])
            # print(f'{d.id} => {d.to_dict()}')

        print(member_names, member_ids, all_timings, status_list)
        payload = {
            'request': request,
            'team_name': team_name,
            'member_ids': member_ids,
            'member_names': member_names,
            'all_timings': all_timings,
            'status_list': status_list
        }
        return templates.TemplateResponse('list_teams.html', payload)
        # return {"API": 'WORKING'}

    except IndexError:
        data = {}
        print("No data found")


class UserRegister(BaseModel):
    UID: str


@app.post("/register/{UID}", dependencies=[Depends(load_data)], response_class=HTMLResponse)
async def register(request: Request, UID: str):
    try:
        print("RESPOND SUCCESS ", g.df.shape)
        details = g.df.loc[g.df['UID'] == UID].to_json(orient='records')
        doc = loads(details[1:-1])
        doc['status'] = "NULL"
        db.collection("participants").document(UID).set(doc)
        return """
            <html>
            <head>
                <title>REGISTRATION</title>
            </head>
            <body style="background-color:green">
                <h1>Registration Completed!</h1>
            </body>
            </html>
            """
    except:
        return """
        <html>
            <head>
                <title>REGISTRATION</title>
            </head>
            <body style="background-color:red">
                <h1>Registration Failed!</h1>
            </body>
            </html>
             """


if __name__ == "__main__":
    uvicorn.run(app, port=8080)

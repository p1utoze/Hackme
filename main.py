import uvicorn
import time
import requests
import pandas as pd
from auth import google_sso
from admin import dashboard
from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import starlette.status as status
from api_globals import GlobalsMiddleware, g
from json import loads
from fastapi.responses import RedirectResponse, HTMLResponse
from admin.utils import db, web_auth
from participants.register import fetch_user_status, check_participant


app = FastAPI(
    title="Hackme API",
    version="1.0.0"
)

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
app.include_router(google_sso.router)
app.include_router(dashboard.router)

templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
async def load_data():
    g.df = pd.read_csv('Final_List.csv')

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, uid: str = None):
    firebase_user_id = request.cookies.get('firebase_token')
    if firebase_user_id:
        return templates.TemplateResponse("dashboard.html", {"request": request})

    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/auth", response_class=RedirectResponse)
async def email_login(request: Request, email: str = Form(...), password: str = Form(...)):
    # HANDLE FOR INCORRECT LOGIN CREDENTIAL
    try:
        user = web_auth.sign_in_with_email_and_password(email, password)
        if request.cookies.get("login") == "required_by_team":
            redirect_url = request.url_for('register_participant').path + f'?uid={request.cookies.get("userId")}'
            response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        else:
            response = RedirectResponse(url=request.url_for("home"), status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="firebase_token", value=user['idToken'], httponly=True)
        return response
    except requests.exceptions.HTTPError as e:
        err_message = loads(e.strerror)['error']['message']
        print("THIS ERROR", err_message)
    #TODO: HANDLE FOR INCORRECT LOGIN CREDENTIAL IN login.html


@app.get("/qr_scan/{uid}", response_class=RedirectResponse)
async def qr_validate(request: Request, uid: str):
    if not request.cookies.get('firebase_token'):
        response = RedirectResponse(url=request.url_for("home"))
        response.set_cookie(key="login", value="required_by_team", httponly=True)
        response.set_cookie(key="userId", value=uid, httponly=True, max_age=1800)
        return response
    redirect_url = request.url_for('register_participant').path + f'?uid={uid}'
    response = RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
    return response


@app.get("/register", dependencies=[Depends(load_data)], response_class=HTMLResponse)
async def register_participant(request: Request, uid: str):
    member_status_code = check_participant(uid)
    if member_status_code == 600:
        entry_time = time.strftime("%d/%m/%Y %I:%M:%S %p", time.gmtime(time.time() + 19800))
        participants = "participants"
        status_data = fetch_user_status(uid, participants, entry_time)
        response = templates.TemplateResponse("update_status.html",
                                              {"request": request, "Details": status_data})
        if request.cookies.get("userId") == uid:
            response.delete_cookie(key="userId")
            response.delete_cookie(key="login")

        return response

    elif member_status_code == 601:
        details = g.df.loc[g.df['UID'] == uid].to_json(orient='records')
        doc = loads(details[1:-1])
        doc['status'] = "NULL"
        return templates.TemplateResponse('master_checkin.html', {"request": request, "Details": doc})

    elif member_status_code == 602:
        return templates.TemplateResponse('registration_status.html',
                                          {"request": request,
                                           "status": "grey",
                                           "message": "Invalid UID. Not scanned from original QR code"})


@app.post("/register/{UID}", dependencies=[Depends(load_data)], response_class=HTMLResponse)
async def register(request: Request, UID: str):
    try:
        print("RESPOND SUCCESS ", g.df.shape)
        details = g.df.loc[g.df['UID'] == UID].to_json(orient='records')
        doc = loads(details[1:-1])
        doc['status'] = "NULL"
        db.collection("participants").document(UID).set(doc)
        response = templates.TemplateResponse('registration_status.html',
                                          {"request": request,
                                           "status": "green",
                                           "message": "Registration Successful!"})
        if request.cookies.get("userId") == UID:
            response.delete_cookie(key="userId")
            response.delete_cookie(key="login")
        return response

    except ValueError as e:
        return templates.TemplateResponse('registration_status.html',
                                          {"request": request,
                                           "status": "red",
                                           "message": "Error in registration"})


if __name__ == "__main__":
    uvicorn.run(app, port=8080)

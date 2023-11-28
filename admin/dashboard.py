# Desc: Admin dashboard routes
import requests
import pandas as pd
from fastapi import FastAPI, Depends, Request, Form, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import starlette.status as status
from pydantic import BaseModel
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
from api_globals import GlobalsMiddleware, g
from json import loads
from fastapi.responses import Response, RedirectResponse, HTMLResponse
from auth.utils import db, web_auth
from .dependencies import get_templates

templates_ = Jinja2Templates(directory="../templates")
router = APIRouter(prefix="/admin")


@router.get("/dashboard", tags=['Admin'])
async def admin_dashboard(request: Request, templates: Jinja2Templates = Depends(get_templates)):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.post("/dashboard", response_class=HTMLResponse)
async def dashboard_details(request: Request, templates: Jinja2Templates = Depends(get_templates), track: str = Form(...), team_id: str = Form(...)):
    member_ids= []
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
        return templates.TemplateResponse('dashboard.html', payload)

    except IndexError:
        data = {}
        print("No data found")


@router.post("/logout", tags=['Admin'], response_class=RedirectResponse)
async def admin_logout(request: Request):
    response = RedirectResponse(url=request.url_for("home"), status_code=status.HTTP_301_MOVED_PERMANENTLY)
    if request.cookies.get("firebase_token"):
        response.delete_cookie(key="firebase_token")
    if request.cookies.get("login") == "required_by_team":
        response.delete_cookie(key="login")
    print(request.cookies.keys())
    return response

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


templates = Jinja2Templates(directory="../templates")

router = APIRouter(prefix="/admin")

@router.get("/dashboard", tags=['Admin'])
async def admin_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.post("/logout", tags=['Admin'], response_class=RedirectResponse)
async def admin_logout(request: Request):
    response = RedirectResponse(url=request.url_for("home"), status_code=status.HTTP_301_MOVED_PERMANENTLY)
    if request.cookies.get("firebase_token"):
        response.delete_cookie(key="firebase_token")
    if request.cookies.get("login") == "required_by_team":
        response.delete_cookie(key="login")
    print(request.cookies.keys())
    return response

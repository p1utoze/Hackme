from firebase_admin import firestore
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from api_globals import g, GlobalsMiddleware
from fastapi.templating import Jinja2Templates
from auth.utils import db
from google.cloud.firestore_v1.base_query import FieldFilter
router = APIRouter(prefix="/v1/teams")
templates = Jinja2Templates(directory="../templates")


def fetch_user_status(uid, participants, entry_time):
    cursor = db.collection(participants)
    query = cursor.where(filter=FieldFilter("UID", "==", uid)).get()
    data = query[0].to_dict()
    status_val, status_color = None, None
    try:
        if data['status'] == "NULL":
            print("Added status entry: IN")
            status_val = "IN"
            status_color = "#404040"
            cursor.document(uid).update({'status': status_val})
            cursor.document(uid).update({'checkin': firestore.ArrayUnion([entry_time])})
        elif data['status'] == "IN":
            print("Added status entry: OUT")
            status_val = "OUT"
            status_color = "#a60000"
            cursor.document(uid).update({'status': status_val})
            cursor.document(uid).update({'checkout': firestore.ArrayUnion([entry_time])})
        elif data['status'] == 'OUT':
            print("Added status entry: IN")
            status_val = "IN"
            status_color = "#1b9c00"
            cursor.document(uid).update({'status': status_val})
            cursor.document(uid).update({'checkin': firestore.ArrayUnion([entry_time])})
    except:
        print("wrong status")
    finally:
        status_data = {"status": status_val,
                        "color": status_color,
                       "fname": data['firstName'],
                       "lname": data['lastName'],
                       "team": data['teamName'],
                       "ID": data['UID']
                       }
        return status_data


@router.get("", tags=['Teams'], response_class=HTMLResponse)
async def master_checkin(request: Request):
    return templates.TemplateResponse("master_checkin.html", {"request": request, "teams": g.teams})


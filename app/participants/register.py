from firebase_admin import firestore
from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from app.api_globals import g
from fastapi.templating import Jinja2Templates
from app.admin.utils import db, FIRESTORE_COLLECTION
from google.cloud.firestore_v1.base_query import FieldFilter

# initialize router object with prefix /v1/teams and templates object
router = APIRouter(prefix="/v1/teams")
templates = Jinja2Templates(directory="../templates")


def check_participant(uid=None, is_admin=None):
    """Check if the participant is registered or not. Three cases:

    1. Already Registered participant in Firestore Database entry - Status: 600
    2. Unregistered participant - Status: 601
    3. Invalid QR Code - Status: 602
    Parameters
    ----------
    uid: str, uid of the participant
    is_admin: bool, if the user is admin or not

    Returns
    -------
    :return: int, status code
    """
    if not uid:
        # The participant is not registered. Wrong QRCODE
        return 602
    uid = uid.strip()

    print(f'"{uid}"')
    # Registered participants
    s = uid in g.df["member_id"].tolist()
    if s:
        cursor = db.collection(FIRESTORE_COLLECTION)
        query = cursor.where(filter=FieldFilter("member_id", "==", uid)).get()

        try:
            data = query[0].to_dict()
            # print(f'{query[0].id} => {data}')
        except IndexError:
            data = {}
            # print("No data found")

        # Check if uid in firestore
        if data:
            print("ALREADY REGISTERED USER. REDIRECTING TO CHECKIN...")
            return 600
        print("NOT REGISTERED. REDIRECTING TO REGISTRATION...")
        return 601

    else:
        # Invalid
        return (
            "INVALID UID",
            {"Error": "INVALID UID FOUND"},
        )


def fetch_user_status(uid, participants, entry_time) -> dict:
    """
    Fetch the user status and update the status in the firestore database.
    The status is updated based on the previous status.
    The three cases are:
    1. IN -> OUT
    2. OUT -> IN
    3. NULL -> IN
    Return the other user details along with the status.
    Parameters
    ----------
    uid: str, uid of the participant
    participants: str, collection name
    entry_time: str, entry time

    Returns
    -------
    :return: dict, status data

    """
    cursor = db.collection(participants)
    query = cursor.where(filter=FieldFilter("member_id", "==", uid)).get()
    data = query[0].to_dict()
    status_val, status_color = None, None
    try:
        if data["status"] == "NULL":
            # print("Added status entry: IN")
            status_val = "IN"
            status_color = "#404040"
            cursor.document(uid).update({"status": status_val})
            cursor.document(uid).update(
                {"checkin": firestore.ArrayUnion([entry_time])}
            )
        elif data["status"] == "IN":
            # print("Added status entry: OUT")
            status_val = "OUT"
            status_color = "#a60000"
            cursor.document(uid).update({"status": status_val})
            cursor.document(uid).update(
                {"checkout": firestore.ArrayUnion([entry_time])}
            )
        elif data["status"] == "OUT":
            # print("Added status entry: IN")
            status_val = "IN"
            status_color = "#1b9c00"
            cursor.document(uid).update({"status": status_val})
            cursor.document(uid).update(
                {"checkin": firestore.ArrayUnion([entry_time])}
            )
    except KeyError as e:
        print("wrong status", e)
    finally:
        status_data = {
            "status": status_val,
            "color": status_color,
            "fname": data["f_name"],
            "lname": data["l_name"],
            "team": data["team_name"],
            "ID": data["member_id"],
        }
        return status_data


@router.get("", tags=["Teams"], response_class=HTMLResponse)
async def master_checkin(request: Request):
    """Master checkin route, renders the master_checkin.html template.

    Parameters
    ----------
    request: Request object

    Returns
    -------
    :return: HTMLResponse object`
    """
    return templates.TemplateResponse(
        "master_checkin.html", {"request": request, "teams": g.teams}
    )

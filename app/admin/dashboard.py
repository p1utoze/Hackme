# Desc: Admin dashboard routes
from fastapi import Depends, Request, Form, APIRouter
from fastapi.templating import Jinja2Templates
import starlette.status as status
from google.cloud.firestore_v1.base_query import FieldFilter
from fastapi.responses import RedirectResponse, HTMLResponse
from app.admin.utils import db, COOKIE_NAME, FIRESTORE_COLLECTION
from .dependencies import get_templates

# initialize router object with prefix /admin
router = APIRouter(prefix="/admin")


@router.get("/dashboard", tags=["Admin"])
async def admin_dashboard(
    request: Request, templates: Jinja2Templates = Depends(get_templates)
):
    """Admin dashboard route, displays all the teams and their members based on
    the query params.

    Parameters
    ----------
    request: Request object
    templates: Jinja2Templates object from dependencies

    Returns
    -------
    :return: HTMLResponse
    """
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.post("/dashboard", response_class=HTMLResponse, tags=["Admin"])
async def dashboard_details(
    request: Request,
    templates: Jinja2Templates = Depends(get_templates),
    team_id: str = Form(...),
):
    """Dashboard details route, displays all the teams and their members based
    on the query params on POST request. The payload is sent to the
    dashboard.html template. The template renders the data in a collapsible
    table format.

    Parameters
    ----------
    request: Request object
    templates: Jinja2Templates object from dependencies
    team_id: str, team code

    Returns
    -------
    :return: HTMLResponse
    """
    member_ids = []
    member_names = []
    all_timings = []
    status_list = []
    team_name = None
    doc = db.collection(FIRESTORE_COLLECTION)
    query = doc.where(filter=FieldFilter("team_id", "==", team_id)).stream()
    try:
        # print(query)
        for d in query:
            # print(d.__dict__)
            details = d.to_dict()
            # print(details)
            member_ids.append(details["member_id"])
            member_names.append(
                " ".join([details["f_name"], details["l_name"]])
            )
            if not team_name:
                team_name = details["team_name"]
            all_timings.append(
                {
                    "IN": details.get("checkin", " "),
                    "OUT": details.get("checkout", ""),
                }
            )
            status_list.append(details["status"])
            # print(f'{d.id} => {d.to_dict()}')

        print(member_names, member_ids, all_timings, status_list)
        payload = {
            "request": request,
            "team_name": team_name,
            "team_details": zip(
                member_ids, member_names, status_list, all_timings
            ),
        }
        return templates.TemplateResponse("dashboard.html", payload)

    except IndexError:
        print("No data found")


@router.post("/logout", tags=["Admin"], response_class=RedirectResponse)
async def admin_logout(request: Request):
    """Admin logout route, deletes the cookie and redirects to the home page.

    Parameters
    ----------
    request: Request object

    Returns
    -------
    :return: RedirectResponse
    """
    response = RedirectResponse(
        url=request.url_for("home"),
        status_code=status.HTTP_301_MOVED_PERMANENTLY,
    )
    if request.cookies.get(COOKIE_NAME):
        response.delete_cookie(key=COOKIE_NAME)
    if request.cookies.get("login") == "required_by_team":
        response.delete_cookie(key="login")
    print(request.cookies.keys())
    return response

import uvicorn
import time
import requests
import pandas as pd
from app.auth import google_sso
from app.admin import dashboard
from fastapi import FastAPI, Depends, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import starlette.status as status
from app.api_globals import GlobalsMiddleware, g
from json import loads
from fastapi.responses import RedirectResponse, HTMLResponse
from app.admin.utils import db, web_auth, COOKIE_NAME
from app.participants.register import fetch_user_status, check_participant
from app.settings import data_path, static_dir, template_dir

# Initialize FastAPI app instance with title and version
app = FastAPI(title="Hackme API", version="1.0.0")

# Add CORS middleware to allow all origins to make requests to this API server
allow_all = ["*"]
app.add_middleware(GlobalsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_all,
    allow_credentials=True,
    allow_methods=allow_all,
    allow_headers=allow_all,
)

# Mount static files and routers to the app instance
app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.include_router(google_sso.router)
app.include_router(dashboard.router)

# Initialize Jinja2 templates for rendering HTML pages
templates = Jinja2Templates(directory=template_dir)


@app.on_event("startup")
async def load_data():
    """Load data from CSV file into memory. This function is called when the
    app starts up. The data is stored in the global variable `g.df` which is
    accessible from any part of the app. This is done to avoid reading the CSV
    file from disk every time a request is made to the API server. The global
    variable initialization is done in the file `app/api_globals.py` which is
    imported at the top of this file.

    :param: None    :return: None
    ----------------
    """
    g.df = pd.read_csv(data_path)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page. This is the first page that is rendered when the
    user visits the website. It checks if the user is logged in or not. If the
    user is logged in, it redirects to the dashboard page. If the user is not
    logged in, it redirects back to the login page based on the session cookie
    stored in the browser (created when the user logs in). The cookie name is a
    environment variable `COOKIE_NAME` which is defined in the file
    `app/admin/utils.py`

    Parameters
    ----------
    :param request: FastAPI Request object

    Returns
    -------
    :return: HTMLResponse object
    """
    firebase_user_id = request.cookies.get(COOKIE_NAME)
    if firebase_user_id:
        return templates.TemplateResponse(
            "dashboard.html", {"request": request}
        )

    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/auth", response_class=RedirectResponse)
async def email_login(
    request: Request, email: str = Form(...), password: str = Form(...)
):
    """Authenticate the user using email and password (Password-based
    authentication). This function is called when the user submits the login
    form on the login page. It uses the Firebase Authentication REST API to
    authenticate the user using email stored in the firebase database and the
    password entered by the user. It also sets a session if the users are
    scanning the QR code for the first time. The session is used to redirect
    the user to the register page after successful login. The session is valid
    for 30 minutes. The session cookie name is `login` and the user id is
    stored in the cookie named `userId`. The cookie name is a environment
    variable `COOKIE_NAME` which is defined.

    Parameters
    ----------
    request: FastAPI Request object
    email: str
    password: str

    Returns
    -------
    :return: RedirectResponse object
    """
    try:
        user = web_auth.sign_in_with_email_and_password(email, password)
        if request.cookies.get("login") == "required_by_team":
            redirect_url = (
                request.url_for("register_participant").path
                + f'?uid={request.cookies.get("userId")}'
            )
            response = RedirectResponse(
                url=redirect_url, status_code=status.HTTP_302_FOUND
            )
        else:
            response = RedirectResponse(
                url=request.url_for("home"), status_code=status.HTTP_302_FOUND
            )
        response.set_cookie(
            key=COOKIE_NAME, value=user["idToken"], httponly=True
        )
        return response
    except requests.exceptions.HTTPError as e:
        err_message = loads(e.strerror)["error"]["message"]
        print("THIS ERROR", err_message)
    # TODO: HANDLE FOR INCORRECT LOGIN CREDENTIAL IN login.html


@app.get("/qr_scan/{uid}", response_class=RedirectResponse)
async def qr_validate(request: Request, uid: str):
    """The endpoint is called when the user scans the QR code. It checks if the
    user is logged in or not. If the user is not logged in, it sets a session
    cookie and redirects to the register page.

    If the user is logged in, it redirects to the register page.
    Two cookies are set in the browser - `login` and `userId`, w
    which are cleared after successful login and participant registration.
    Parameters
    ----------
    request: FastAPI Request object
    uid: str

    Returns
    -------
    :return: RedirectResponse object
    """
    if not request.cookies.get(COOKIE_NAME):
        response = RedirectResponse(url=request.url_for("home"))
        response.set_cookie(
            key="login", value="required_by_team", httponly=True
        )
        response.set_cookie(
            key="userId", value=uid, httponly=True, max_age=1800
        )
        return response
    redirect_url = request.url_for("register_participant").path + f"?uid={uid}"
    response = RedirectResponse(
        url=redirect_url, status_code=status.HTTP_302_FOUND
    )
    return response


@app.get(
    "/register", dependencies=[Depends(load_data)], response_class=HTMLResponse
)
async def register_participant(request: Request, uid: str):
    """Render the register page. This page is rendered when the user scans the
    QR code for the first time. It checks if the user is logged in or not. If
    the user is not logged in, it redirects to the login page. If the user is
    logged in, it renders the register page. The user id is the UID of the
    participant which is passed as a query parameter. `check_participant`
    function returns the status code of the participant to redirect to the
    appropriate page.

    Parameters
    ----------
    request: FastAPI Request object
    uid: str

    Returns
    -------
    :return: HTMLResponse object
    """
    member_status_code = check_participant(uid)
    if (
        member_status_code == 600
    ):  # Update status page for already registered participants with timestamp
        entry_time = time.strftime(
            "%d/%m/%Y %I:%M:%S %p", time.gmtime(time.time() + 19800)
        )
        participants = "participants"
        status_data = fetch_user_status(uid, participants, entry_time)
        response = templates.TemplateResponse(
            "update_status.html", {"request": request, "Details": status_data}
        )
        if request.cookies.get("userId") == uid:
            response.delete_cookie(key="userId")
            response.delete_cookie(key="login")

        return response

    elif (
        member_status_code == 601
    ):  # Fetch details from database and render registration form
        details = g.df.loc[g.df["UID"] == uid].to_json(orient="records")
        doc = loads(details[1:-1])
        doc["status"] = "NULL"
        return templates.TemplateResponse(
            "master_checkin.html", {"request": request, "Details": doc}
        )

    elif (
        member_status_code == 602
    ):  # Not scanned from original QR code generated by the organizer
        return templates.TemplateResponse(
            "registration_status.html",
            {
                "request": request,
                "status": "grey",
                "message": "Invalid UID. Not scanned from original QR code",
            },
        )


@app.post(
    "/register/{UID}",
    dependencies=[Depends(load_data)],
    response_class=HTMLResponse,
)
async def register(request: Request, UID: str):
    """Register the participant. This function is called when the user submits
    the register form on the register page. It updates the participant details
    in the firebase database and renders the registration status page. The user
    id is the UID of the participant which is passed as a query parameter.
    Remove the session cookies required if the user hasn't logged in before
    scanning the QR code.

    Parameters
    ----------
    request
    UID

    Returns
    -------
    :return: HTMLResponse object
    """
    try:
        # print("RESPOND SUCCESS ", g.df.shape)
        details = g.df.loc[g.df["UID"] == UID].to_json(orient="records")
        doc = loads(details[1:-1])
        doc["status"] = "NULL"
        db.collection("participants").document(UID).set(doc)
        response = templates.TemplateResponse(
            "registration_status.html",
            {
                "request": request,
                "status": "green",
                "message": "Registration Successful!",
            },
        )
        if request.cookies.get("userId") == UID:
            response.delete_cookie(key="userId")
            response.delete_cookie(key="login")
        return response

    except ValueError:
        return templates.TemplateResponse(
            "registration_status.html",
            {
                "request": request,
                "status": "red",
                "message": "Error in registration",
            },
        )


if __name__ == "__main__":
    uvicorn.run(app, port=8080)

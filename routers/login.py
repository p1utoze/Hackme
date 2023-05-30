from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRouter
from routers.login_form import LoginForm
from fastapi import Depends, Request
from fastapi.exception_handlers import HTTPException
templates = Jinja2Templates(directory="templates")

router = APIRouter(include_in_schema=False)

@router.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login/")
async def login(request: Request):
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
        try:
            form.__dict__.update(msg="Login Successful :)")
            response = templates.TemplateResponse("home.html", form.__dict__)
            # login_for_access_token(response=response, form_data=form, db=db)
            return response
        except HTTPException:
            form.__dict__.update(msg="")
            form.__dict__.get("errors").append("Incorrect Email or Password")
            return templates.TemplateResponse("login.html", form.__dict__)
    return templates.TemplateResponse("login.html", form.__dict__)
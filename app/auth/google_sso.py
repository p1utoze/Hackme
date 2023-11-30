from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO
from starlette.requests import Request
import os
import firebase_admin
from firebase_admin import auth as fb_auth
from app.admin.utils import (
    GOOGLE_CLIENT_SECRET,
    GOOGLE_CLIENT_ID,
    HOST,
    COOKIE_NAME,
)


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # Only for development


def get_google_sso() -> GoogleSSO:
    return GoogleSSO(
        GOOGLE_CLIENT_ID,
        GOOGLE_CLIENT_SECRET,
        f"{HOST}/v1/google/callback",
        allow_insecure_http=True,  # Disable this in production
    )


router = APIRouter(prefix="/v1/google")


@router.get("/login", tags=["Google SSO"])
async def auth_init(sso=Depends(get_google_sso)):
    """Initialize auth and redirect."""
    return await sso.get_login_redirect()


@router.get("/callback", response_class=RedirectResponse, tags=["Google SSO"])
async def auth_callback(request: Request, sso=Depends(get_google_sso)):
    """Verify login."""
    user = await sso.verify_and_process(request)
    try:
        valid_user = fb_auth.get_user_by_email(user.email)
        user_id_token = fb_auth.create_custom_token(valid_user.uid)
        print(valid_user)
        print(request.cookies.get("login"))
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
            key=COOKIE_NAME,
            value=user_id_token.decode(),
            httponly=True,
            max_age=1800,
        )
        return response

    except firebase_admin._auth_utils.UserNotFoundError:
        redirect_url = request.url_for("root") + "?x-error=Unauthorized+access"
        return RedirectResponse(
            redirect_url,
            status_code=status.HTTP_302_FOUND,
            headers={"x-error": "Unauthorized access"},
        )

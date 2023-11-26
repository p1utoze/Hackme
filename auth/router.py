from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi_sso.sso.google import GoogleSSO
from starlette.requests import Request
from dotenv import load_dotenv
from pathlib import Path
import os
import firebase_admin
from firebase_admin import auth as fb_auth, credentials


directory_path = Path(__file__).parent
env_file_path = directory_path.parent / '.env'

load_dotenv()
GOOGLE_CLIENT_ID =  os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET =  os.getenv("GOOGLE_CLIENT_SECRET")
HOST = os.getenv("HOSTNAME_URI")


firebaseConfig = {
  "apiKey": "AIzaSyDYt2Mj95NipbFOhBMb3jDsdUoXi7YFFUc",
  "authDomain": "hackme-60c66.firebaseapp.com",
  "databaseURL": "https://hackme-60c66-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "hackme-60c66",
  "storageBucket": "hackme-60c66.appspot.com",
  "messagingSenderId": "505276403628",
  "appId": "1:505276403628:web:4e292a5a0395c348543409",
  "measurementId": "G-QR40ZRVFT3"
}
firebase_app = firebase_admin.initialize_app(firebaseConfig)

cred = credentials.Certificate('hackme.json')
fir_app = firebase_admin.initialize_app(cred)


def get_google_sso() -> GoogleSSO:
    return GoogleSSO(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, f"{HOST}/v1/google/callback")


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1' # Only for development


def get_google_sso() -> GoogleSSO:
    return GoogleSSO(GOOGLE_CLIENT_ID,
                     GOOGLE_CLIENT_SECRET,
                     f"{HOST}/v1/google/callback",
                     allow_insecure_http=True  # Disable this in production
                     )


router = APIRouter(prefix="/v1/google")


@router.get("/login", tags=['Google SSO'])
async def auth_init(sso=Depends(get_google_sso)):
    """Initialize auth and redirect"""
    return await sso.get_login_redirect()


@router.get("/callback", response_class=RedirectResponse, tags=['Google SSO'])
async def auth_callback(request: Request, sso=Depends(get_google_sso)):
    """Verify login"""
    user = await sso.verify_and_process(request)
    print(user)
    try:
        valid_user = fb_auth.get_user_by_email(user.email)
        user_id_token = fb_auth.create_custom_token(valid_user.uid)
        print(valid_user)
        response = RedirectResponse(url="/")
        response.set_cookie(key="firebase_token", value=user_id_token.decode(), httponly=True, max_age=1800)
        return response
    except firebase_admin._auth_utils.UserNotFoundError:
        redirect_url = request.url_for('root') + '?x-error=Invalid+credentials'
        return RedirectResponse(redirect_url, status_code=status.HTTP_302_FOUND,
                                headers={"x-error": "Invalid credentials"})

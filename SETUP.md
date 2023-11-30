# Project Setup Guide
This section is for the setting the environment variables used by the application for development and production and also for setting up the organizing team database for application access.


---
## Environment Variables

- **SESSION_COOKIE_NAME:** Name of the cookie used to store the session id.
<br>
<br>
- **HOSTNAME_URL:** Hostname of the application. Used for initializing redirect_uri parameter for Google OAuth2 in the app
<br>
<br>
- **GOOGLE_CLIENT_ID:** Google client id for OAuth2 authentication.
    1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  2. Create a new project
  3. Go to APIs & Services > Credentials
  4. Create a new OAuth Client ID
  5. Select Web Application
  6. Add the redirect URI in the Authorized redirect URIs section. This must be the same as the HOSTNAME_URL
  7. Click on save and download the credentials json file
  8. Copy the client id from the json file and paste it in the GOOGLE_CLIENT_ID variable
<br>
<br>
- **GOOGLE_CLIENT_SECRET:** Copy the client secret from the same json file and paste it in the GOOGLE_CLIENT_SECRET variable
<br>
<br>
- **FIREBASE_SERVICE_ACCOUNT:**
  1. Go to [Firebase Console](https://console.firebase.google.com/)
  2. Create a new project
  3. Go to Project Settings
  4. Go to Service Accounts
  5. Click on Generate new private key
  6. Download the json file and convert it to string
    ```
    import json
    with open('path/to/serviceAccountKey.json') as f:
        data = json.load(f)
    print(json.dumps(data))
    ```
  7. Copy the string and paste it in the FIREBASE_SERVICE_ACCOUNT variable
<br>
<br>
- **FIREBASE_CONFIG:**
  1. Create a new web app in the firebase project
  2. copy the config object from the firebaseConfig variable in the firebase initialization script.
  3. Paste it in the FIREBASE_CONFIG variable

---

## Setting up Organizing Team Database

- Go to your firebase project
- Go to Authentication
- Click on get started
- Under the "Native providers" section, click on "Email/Password" and enable it. Leave the other settings as default
- Click on "Add user" and create a new user with email and password
- Done! Now only the users with the email and password can access the application through google sign-in or email and password sign-in method

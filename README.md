<p align="center">
  <img src="https://results.pre-commit.ci/badge/github/p1utoze/Hackme/main.svg">
</p>
  
# Hackme
A minimalistic open-source web-application that serves as hackathon registration and participant status monitoring. Initally developed as a event management tool for [Hackaventus](https://hackaventus.com/)- A national level hackathon. It is designed to handle large amount of user registrations.

## Features

- Instant QR Code Registration
- Restricted Access for Organizing Team ✉️
- Single scan, multiple functionalities 📨
- Supports Google SSO and Firebase Auth with email and password 🤔
- Participant management dashboard
- Automatic participant status update through ID scan

## Get started
To use this app locally, pull the docker image and run on port 5050

### Prerequisites

- Install project dependencies using pip
```
pip install -r requirements.txt
```
- Rename the `.env.template` to `.env` and replace the placeholders. Refer [Environment Variables configuration](SETUP.md/#environment-variables-configuration
) for more details.

- Add the users who can access the application to the firebase project. Refer [Setting up Organizing Team Database](SETUP.md/#setting-up-organizing-team-database) for more details.

### Usage

- **Uvicorn:** To run the app locally with uvicorn server on port `<port>`.
```
uvicorn app.main:app --reload --port <port>
```
- **Docker:** To run the app locally with docker on port `<port>`.
```
$ docker pull p1utoze/hackme:v1.0
$ docker run -p <port>:5050 --env-file .env p1utoze/hackme:v1.0
```
**NOTE:**  Make sure the callback url port is same as the port specified in the command. Refer [Environment Variables configuration](SETUP.md/#environment-variables-configuration
) for more details.

### Python

Needs: Python 3.X, virtualenv

Stable at Python v.3.8.X and 3.10 (tested at Python 3.8.17 and 3.10)

### Roadmap
Currently, I have mentioned the features that I have planned to implement in the future in the issues. If you have any suggestions, please feel free to open an issue.
### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

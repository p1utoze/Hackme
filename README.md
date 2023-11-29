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
```
$ docker pull p1utoze/hackme:v1.0
```

## Docker-Compose

Needs: Docker, Docker-Compose

- `./install.sh` (Creates virtualenviroment, install requirements.txt and migrates DB)
- `docker-compose up` (Starts server)

That is all! 😃 If you need to run any python command just do as the following examples:

- Install new library: `docker-compose run python -m pip install [library]`
- Make migrations: `docker-compose run python manage.py makemigrations`
- Migrate: `docker-compose run python manage.py migrate`

### Python

Needs: Python 3.X, virtualenv

Stable at Python v.3.8.X and 3.10 (tested at Python 3.8.17 and 3.10)

- `git clone git@github.com:HackAssistant/hackassistant.git && cd hackassistant`
- `virtualenv env --python=python3`
- `source ./env/bin/activate`
- `pip install -r requirements.txt`
- `python manage.py migrate`
- `python manage.py createadmin` (creates admin to manage all the app: CUSTOM COMMAND!)
- `python manage.py runserver localhost:8000` (specifies to localhost, since admin is created under that specific domain, otherwise it wont work)

FROM python:3.10-slim-buster
LABEL authors="p1utoze"

#
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 5050

CMD ["gunicorn", "app.main:app", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:5050", "--forwarded-allow-ips='*'"]



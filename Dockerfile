FROM python:3.10-slim-buster
LABEL authors="p1utoze"

# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY ./requirements.txt /code/requirements.txt

# install dependencies
RUN pip install --no-cache-dir -r /code/requirements.txt

# copy the content of the local FastAPI app directory to the working directory
COPY ./app /code/app

# expose port 5050
EXPOSE 5050

# command to run on container start
CMD ["gunicorn", "app.main:app", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:5050", "--forwarded-allow-ips='*'"]

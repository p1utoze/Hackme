FROM python:3.9
LABEL authors="p1utoze"

WORKDIR aventus/

COPY requirements.txt .

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5050

CMD ["gunicorn", "main:app", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:5050", "--forwarded-allow-ips='*'"]



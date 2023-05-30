FROM python:3.9
LABEL authors="p1utoze"

WORKDIR aventus/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:3000", "--forwarded-allow-ips='*'"]



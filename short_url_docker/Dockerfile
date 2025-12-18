FROM python:3.12.3

WORKDIR /app
COPY short_url short_url

WORKDIR /app/short_url

RUN python -m pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

CMD ["uvicorn", "main:app",  "--port", "8000"]

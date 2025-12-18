FROM python:3.12.3

WORKDIR /app
COPY to_do_list to_do_list

WORKDIR /app/to_do_list

RUN python -m pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir

EXPOSE 8000

CMD ["uvicorn", "main:app",  "--port", "8000"]

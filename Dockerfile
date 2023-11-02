FROM python:3.10.11

WORKDIR /todos

COPY . /todos

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
FROM python:3.9.1

WORKDIR D:/Dockerdirs/chat/app

COPY ./requirements.txt D:/Dockerdirs/chat/requirements.txt

RUN pip install --no-cache-dir --upgrade -r D:/Dockerdirs/chat/requirements.txt

COPY ./app D:/Dockerdirs/chat/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

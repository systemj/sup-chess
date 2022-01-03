FROM python:3.9-slim-bullseye
RUN apt update && apt upgrade -y && apt install -y gnuchess

WORKDIR /app
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


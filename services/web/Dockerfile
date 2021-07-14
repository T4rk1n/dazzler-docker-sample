FROM python:3.9.5-slim-buster

WORKDIR /usr/src/app

RUN apt-get update
RUN pip install --upgrade pip

COPY . /usr/src/app

RUN pip install -r requirements.txt

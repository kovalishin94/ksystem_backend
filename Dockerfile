FROM ubuntu:20.04

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

COPY requirements.txt ./
RUN apt-get update && apt-get install -y python3-dev libxml2-dev python3-pip build-essential
RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT [ "daphne" ]
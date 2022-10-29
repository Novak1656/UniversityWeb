FROM python:3.10.7

WORKDIR /usr/src/university

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/university/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/university/
FROM python:3.6

LABEL Name="study.plus.or.kr"
LABEL Version="0.1"
LABEL Maintainer="yechan@postech.ac.kr"

ENV PYTHONUNBUFFERED 1
RUN mkdir /entry
ADD ./entry /entry/
ADD requirements.txt /entry/
RUN pip install -r /entry/requirements.txt
RUN mkdir /static && mkdir /upload && mkdir /code
ADD ./src /code/
WORKDIR /code

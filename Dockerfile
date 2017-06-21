FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /entry
ADD ./entry /entry/
ADD requirements.txt /entry/
RUN pip install -r /entry/requirements.txt
RUN mkdir /static
RUN mkdir /code
ADD ./src /code/
WORKDIR /code
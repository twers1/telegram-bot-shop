FROM python:3.11.1-slim-buster as builder

ARG TOKEN
ARG ADMIN_ID
ARG DB_URI

ENV TOKEN=$TOKEN
ENV ADMIN_ID=$ADMIN_ID
ENV DB_URI=$DB_URI

WORKDIR /app

COPY requirements.txt requirements.txt
COPY src src
COPY bot.py bot.py

RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "bot.py"]
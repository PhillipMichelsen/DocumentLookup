FROM python:3.10-slim

WORKDIR /src

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /src/app
#COPY ./sentence_models /src/sentence_models

ENV PYTHONPATH /src
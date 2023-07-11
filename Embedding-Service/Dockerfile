FROM python:3.10

WORKDIR /src

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /src/app

# Uncomment if embedding_models downloaded on local machine
COPY ./embedding_models /src/embedding_models

ENV PYTHONPATH /src
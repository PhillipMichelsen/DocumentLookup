FROM python:3.10-alpine

WORKDIR /src

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /src/app

ENV PYTHONPATH /src

CMD ["python", "app/main.py"]
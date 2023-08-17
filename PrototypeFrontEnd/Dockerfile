FROM python:3.10-slim

WORKDIR /src

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /src/app

ENV PYTHONPATH /src

EXPOSE 8501

CMD ["streamlit", "run", "app/main.py", "--server.maxUploadSize=1028"]
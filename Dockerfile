FROM python:3.12

WORKDIR /trading-conversion-bot

COPY ../trading-conversion-bot .

RUN apt-get update && \
    apt-get install -y wait-for-it && \
    pip install -r requirements.txt

EXPOSE 8000
FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y gcc

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV OPENAI_API_KEY=""
ENV TELEGRAM_TOKEN=""
ENV TELEGRAM_CHAT_ID=""
ENV ZAPIER_WEBHOOK_URL=""

CMD [ "python", "main.py" ]

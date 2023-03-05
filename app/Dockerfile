FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y gcc

WORKDIR /app

COPY requirements.txt .

RUN apt-get update
RUN apt-get update && apt-get install -y \
    libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg libavcodec-extra libssl-dev \
    && rm -rf /var/lib/apt/lists/*
RUN apt-get install build-essential -y
RUN pip install Cmake
RUN pip install -r requirements.txt

COPY . .

ENV OPENAI_API_KEY=""
ENV TELEGRAM_TOKEN=""
ENV TELEGRAM_CHAT_ID=""
ENV ZAPIER_WEBHOOK_URL=your_zapier_webhook_url
ENV GOOGLE_APPLICATION_CREDENTIALS=your_google_credentials_file_path
ENV GOOGLE_PROJECT_ID=your_google_project_id


CMD [ "python", "main.py" ]

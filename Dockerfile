FROM python:3.9-slim

RUN apt-get update && apt-get install -y gcc

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

CMD ["python", "app.py"]

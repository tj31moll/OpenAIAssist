# Use the official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Expose the port that the application will listen on
EXPOSE 5000

# Define environment variables
ENV OPENAI_API_KEY=<your-openai-api-key>
ENV TELEGRAM_TOKEN=<your-telegram-bot-token>
ENV TELEGRAM_CHAT_ID=<your-telegram-chat-id>

# Run the application
CMD ["python", "main.py"]

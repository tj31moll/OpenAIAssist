import openai
import os
import telegram
import speech_recognition as sr
import pyttsx3
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import requests
from google.oauth2.credentials import Credentials
from google.assistant.library import Assistant
from google.assistant.library.event import EventType

# Define environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]
telegram_token = os.environ["TELEGRAM_TOKEN"]
telegram_chat_id = os.environ["TELEGRAM_CHAT_ID"]
zapier_webhook_url = os.environ["ZAPIER_WEBHOOK_URL"]
google_project_id = os.environ["GOOGLE_PROJECT_ID"]
google_credentials = os.environ["GOOGLE_APPLICATION_CREDENTIALS"]

# Initialize ChatBot and train with corpus
chatbot = ChatBot('MyChatBot')
trainer = ChatterBotCorpusTrainer(chatbot)
trainer.train('chatterbot.corpus.english')

# Initialize speech recognition and text-to-speech engines
r = sr.Recognizer()
engine = pyttsx3.init()
bot = telegram.Bot(token=telegram_token)

def main():
    log_file = open("conversation_log.txt", "a")
    with Assistant(credentials=Credentials.from_authorized_user_info(info=None), project_id=google_project_id) as assistant:
        for event in assistant.start():
            if event.type == EventType.ON_START_FINISHED:
                log_file.write("Assistant: Ready!\n")
                print('Assistant ready')
            elif event.type == EventType.ON_CONVERSATION_TURN_STARTED:
                print('Assistant listening')
            elif event.type == EventType.ON_RECOGNIZING_SPEECH_FINISHED:
                user_input = event.args['text']
                log_file.write("User: " + user_input + "\n")
                if user_input.lower() == 'bye':
                    assistant.stop_conversation()
                    speak("Goodbye!")
                    log_file.write("Assistant: Goodbye!\n")
                    break
                elif user_input.lower().startswith('hey google'):
                    send_to_zapier(user_input)
                elif user_input.lower().startswith('chatbot'):
                    response = chatbot.get_response(user_input[7:])
                    send_to_telegram(response)
                    assistant.send_text_query(response)
                    speak(response)
                    log_file.write("Assistant: " + str(response) + "\n")
                elif user_input.lower().startswith('openai'):
                    response = generate_response(user_input[7:])
                    send_to_telegram(response)
                    assistant.send_text_query(response)
                    speak(response)
                    log_file.write("Assistant: " + str(response) + "\n")
                else:
                    response = chatbot.get_response(user_input)
                    send_to_telegram(response)
                    assistant.send_text_query(response)
                    speak(response)
                    log_file.write("Assistant: " + str(response) + "\n")
            elif event.type == EventType.ON_CONVERSATION_TURN_FINISHED:
                print('Assistant idle')
    log_file.close()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5
    )
    message = response.choices[0].text.strip()
    return message

def send_to_zapier(message):
    data = {"message": message}
    response = requests.post(zapier_webhook_url, data=data)
    print(response.text)

def send_to_telegram(message):
    bot.send_message(chat_id=telegram_chat_id, text=message)

if __name__ == '__main__':
    main()

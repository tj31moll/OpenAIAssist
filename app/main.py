import openai
import os
import telegram
import speech_recognition as sr
import pyttsx3
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainerimport
import requests

# Define environment variables
openai.api_key = os.environ["OPENAI_API_KEY"]
telegram_token = os.environ["TELEGRAM_TOKEN"]
telegram_chat_id = os.environ["TELEGRAM_CHAT_ID"]
zapier_webhook_url = os.environ["ZAPIER_WEBHOOK_URL"]

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
    while True:
        user_input = listen()
        log_file.write("User: " + user_input + "\n")
        if user_input.lower() == 'bye':
            speak("Goodbye!")
            log_file.write("Assistant: Goodbye!\n")
            break
        elif user_input.lower().startswith('hey google'):
            send_to_zapier(user_input)
        elif user_input.lower().startswith('chatbot'):
            response = chatbot.get_response(user_input[7:])
            send_to_telegram(response)
            speak(response)
            log_file.write("Assistant: " + str(response) + "\n")
        elif user_input.lower().startswith('openai'):
            response = generate_response(user_input[7:])
            send_to_telegram(response)
            speak(response)
            log_file.write("Assistant: " + str(response) + "\n")
        else:
            response = chatbot.get_response(user_input)
            send_to_telegram(response)
            speak(response)
            log_file.write("Assistant: " + str(response) + "\n")
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

def listen():
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said: " + text)
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

def send_to_zapier(message):
    data = {"message": message}
    response = requests.post(zapier_webhook_url, data=data)
    print(response.text)

def send_to_telegram(message):
    bot.send_message(chat_id=telegram_chat_id, text=message)

if __name__ == '__main__':
    main()

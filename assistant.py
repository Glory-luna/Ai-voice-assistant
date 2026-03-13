import speech_recognition as sr
import pyttsx3
import requests
import webbrowser
import os

# -------------------------
# Voice Engine
# -------------------------
engine = pyttsx3.init()
engine.setProperty('rate',170)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

# -------------------------
# Voice Input
# -------------------------
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print("You:", text)
        return text.lower()
    except:
        speak("Sorry, I didn't understand.")
        return ""

# -------------------------
# AI Response (Ollama)
# -------------------------
def ask_ai(question):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model":"tinyllama",
                "prompt":f"Answer briefly: {question}",
                "stream":False,
                "options":{
                    "num_predict":25,
                    "temperature":0.3
                }
            }
        )

        return response.json()["response"]

    except:
        return "Sorry, I couldn't connect to the AI."

# -------------------------
# Memory System
# -------------------------
memory = {}

# -------------------------
# Command Processor
# -------------------------
def run_command(text):

    if "open chrome" in text:
        speak("Opening Chrome")
        os.system("start chrome")

    elif "open vs code" in text:
        speak("Opening VS Code")
        os.system("code")

    elif "open youtube" in text:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "search" in text:
        query = text.replace("search","")
        webbrowser.open(f"https://www.google.com/search?q={query}")
        speak("Searching Google")

    elif "remember that" in text:
        fact = text.replace("remember that","")
        memory["fact"] = fact
        speak("I will remember that")

    elif "what did i tell you" in text:
        speak(memory.get("fact","You didn't tell me anything yet"))

    else:
        answer = ask_ai(text)
        speak(answer)

# -------------------------
# Main Program
# -------------------------

speak("Hello Luna. I am your assistant.")

while True:

    user = input("\nType your question or type 'voice': ").lower()

    if user == "voice":
        user = listen()

    if user == "exit":
        speak("Goodbye Luna")
        break

    run_command(user)
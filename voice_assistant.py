import pyttsx3
import speech_recognition as sr
import datetime
import os
import wikipedia
import webbrowser
import pywhatkit
import pyjokes
import ctypes
import threading
import tkinter as tk
from tkinter import scrolledtext

# --- Initialize Speech Engine ---
engine = pyttsx3.init()
engine.setProperty('rate', 175)

# --- Speak Function ---
def speak(audio):
    update_gui(f"🗣️ Echo: {audio}")
    engine.say(audio)
    engine.runAndWait()

# --- Update GUI ---
def update_gui(text):
    text_area.insert(tk.END, text + "\n")
    text_area.see(tk.END)

# --- Listen for Commands ---
def takeCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        update_gui("🎤 Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio, language='en-in')
            update_gui(f"🗨️ You: {query}")
            return query.lower()
        except sr.UnknownValueError:
            update_gui("Sorry, I didn't catch that.")
        except sr.RequestError:
            update_gui("Speech service error.")
    return None

# --- Execute Commands ---
def execute_tasks(query):
    global notes

    if query is None:
        return

    if 'time' in query:
        speak(datetime.datetime.now().strftime("%H:%M:%S"))

    elif 'date' in query:
        speak(datetime.datetime.now().strftime("%A, %d %B %Y"))

    elif 'wikipedia' in query:
        try:
            speak("Searching Wikipedia...")
            result = wikipedia.summary(query.replace("wikipedia", ""), sentences=2)
            speak(result)
        except wikipedia.exceptions.DisambiguationError as e:
            speak("There are multiple results. Please be more specific.")
        except wikipedia.exceptions.PageError:
            speak("Sorry, I couldn't find anything on Wikipedia.")

    elif 'play' in query:
        song = query.replace("play", "").strip()
        speak(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)

    elif 'search' in query:
        search_query = query.replace("search", "").strip()
        speak(f"Searching Google for {search_query}")
        pywhatkit.search(search_query)

    elif 'open notepad' in query:
        os.system("notepad")

    elif 'open command prompt' in query:
        os.system("start cmd")

    elif 'open instagram' in query:
        webbrowser.open("https://www.instagram.com")

    elif 'weather' in query:
        speak("Opening Google Weather.")
        webbrowser.open("https://www.google.com/search?q=weather")

    elif 'joke' in query:
        speak(pyjokes.get_joke())

    elif 'shutdown' in query:
        speak("Shutting down the system.")
        os.system("shutdown /s /t 1")

    elif 'restart' in query:
        speak("Restarting the system.")
        os.system("shutdown /r /t 1")

    elif 'lock' in query:
        speak("Locking the system.")
        ctypes.windll.user32.LockWorkStation()

    elif 'screenshot' in query:
        os.system("snippingtool")

    elif 'remember this' in query:
        speak("What should I remember?")
        notes = takeCommand()
        if notes:
            speak("I will remember that.")
        else:
            speak("I didn't hear anything to remember.")

    elif 'what did i remember' in query:
        if notes:
            speak(f"You told me to remember: {notes}")
        else:
            speak("I don't have anything remembered yet.")

    elif 'who built you' in query:
        speak("I was built by Dua.")

    elif 'exit' in query:
        speak("Goodbye!")
        root.quit()

    else:
        speak("Sorry, I didn't understand.")

# --- Background Listening ---
def start_listening():
    while True:
        query = takeCommand()
        execute_tasks(query)

# --- Start Listening Thread ---
def start_listening_thread():
    threading.Thread(target=start_listening, daemon=True).start()

# --- GUI Setup ---
root = tk.Tk()
root.title("Echo Voice Assistant")
root.geometry("400x500")
root.config(bg="#222222")

tk.Label(root, text="🔹 Echo Voice Assistant 🔹", font=("Arial", 16), bg="#222222", fg="white").pack(pady=10)
text_area = scrolledtext.ScrolledText(root, width=45, height=20, font=("Arial", 12), bg="#333333", fg="white", wrap=tk.WORD)
text_area.pack(pady=10)

# --- Start Button ---
tk.Button(root, text="🎤 Start Listening", font=("Arial", 14), bg="#444444", fg="white", command=start_listening_thread).pack(pady=10)

# --- Run GUI ---
notes = ""  # Initialize notes variable
speak("Echo is ready!")
root.mainloop()

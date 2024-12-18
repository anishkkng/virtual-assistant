import openai
from apikey import api_data  
import pyttsx3
import speech_recognition as sr
import webbrowser
import sys
import datetime
import wikipedia
import os
import random
openai.api_key = api_data
def Reply(question):
    messages = [
        {"role": "system", "content": "You are Jarvis, an AI assistant."},
        {"role": "user", "content": question}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200
        )
        answer = response.choices[0].message['content'].strip()
        return answer
    except openai.error.APIError as e:
        return "I'm currently unavailable, please try again later." 
    except openai.error.AuthenticationError:
        return "Authentication Error: Check your API key."
    except openai.error.RateLimitError:
        return "I'm currently unavailable, please try again later."  
    except Exception as e:
        return f"Unexpected error: {e}"
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
def speak(text):
    engine.say(text)
    engine.runAndWait()
speak("NAMASKAR,HOW CAN I HELP YOU")
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Say that again...")
        return "None"
    return query
def tell_time():
    now = datetime.datetime.now()
    time_str = now.strftime("%H:%M:%S")
    date_str = now.strftime("%Y-%m-%d")
    return f"The current time is {time_str} and today's date is {date_str}"
def play_song(song_name):
    song = '+'.join(song_name.split())
    webbrowser.open(f"https://www.youtube.com/results?search_query={song}")
def tell_joke():
    jokes = [
        "Why don't skeletons fight each other? They don't have the guts!",
        "What do you call fake spaghetti? An impasta!",
        "Why did the scarecrow win an award? Because he was outstanding in his field!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised!"
    ]
    return random.choice(jokes)
if __name__ == '__main__':
    while True:
        query = takeCommand().lower()

        if query == "none":
            continue  

        ans = Reply(query)
        print(ans)
        speak(ans)
        if 'open youtube' in query:
            webbrowser.open("https://www.youtube.com")
        
        if 'open google' in query:
            webbrowser.open("https://www.google.com")
        
        if 'open instagram' in query:
            webbrowser.open("https://www.instagram.com")
        
        if 'open linkedin' in query:
            webbrowser.open("https://www.linkedin.com")
        
        if 'bye' in query:
            speak("Goodbye!")
            sys.exit()
        
        if 'tell me the date and time' in query:
            time_and_date = tell_time()
            print(time_and_date)
            speak(time_and_date)
        
        if 'play song' in query:
            speak("What song would you like to play?")
            song_name = takeCommand().lower()
            play_song(song_name)
        
        if 'tell me a joke' in query:
            joke = tell_joke()
            print(joke)
            speak(joke)
        
        if 'search wikipedia' in query:
            speak("What do you want to search on Wikipedia?")
            search_query = takeCommand().lower()
            try:
                result = wikipedia.summary(search_query, sentences=2)
                print(result)
                speak(result)
            except wikipedia.exceptions.DisambiguationError as e:
                speak(f"There are multiple results for your query. Here are some options: {e.options}")
            except wikipedia.exceptions.HTTPTimeoutError:
                speak("Sorry, I could not connect to Wikipedia. Please try again later.")
            except Exception as e:
                speak(f"Sorry, I couldn't find any information. {str(e)}")

import smtplib
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[0].id)
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hours = int(datetime.datetime.now().hour)  # hour have time 0 to 24
    if hours >= 0 and hours < 12:
        speak("Good Morning!")
    elif hours >= 12 and hours < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Hello, I am Your Device System. Please tell me how may I help you")


def takeCommand():
    # It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(f"Listening.....")
        r.pause_threshold = 1  # for more knowledge open pause_threshold by Ctrl key
        audio = r.listen(source)
    try:
        print("Recognizing.....")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)
        print("Say that again please..")
        return "None"
    return query


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('Sender Email id', 'Sender password')
    server.sendmail('Sender Email id', to, content)
    server.close()


if __name__ == "__main__":
    speak("PRIYANSH")
    wishMe()
    while True:
        query = takeCommand().lower()
# Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak('searching Wikipedia.....')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)
        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
        elif 'open google' in query:
            webbrowser.open("google.com")
        elif 'open stackoverflow' in query:
            webbrowser.open("google.com")
        elif 'play music' in query:
            music_dir = 'D:\\Non Critical\\songs\\Favorite Songs2'  # Make songs directory
            songs = os.listdir(music_dir)
            print(songs)
            # use random module
            os.startfile(os.path.join(music_dir, songs[0]))
        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")
        elif 'open code' in query:
            code_path = "C:\\Program Files\\Microsoft VS Code\\Code.exe"
            os.startfile(code_path)
        elif 'send email' in query:
            try:
                speak("What should I say?")
                content = takeCommand()
                to = "Receiver Email id"  # 3
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry i am not able to send this email at that moment")
        elif 'quit' in query:
            exit()

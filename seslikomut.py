from email.mime import audio
import webbrowser
from async_timeout import timeout
import speech_recognition as sr
from datetime import datetime
import time
from gtts import gTTS
from playsound import playsound
import random
import os
import httplib2
import json
import sqlite3 as sl
r = sr.Recognizer()

http = httplib2.Http(timeout=1)

firstDb = sl.connect("Database.db", check_same_thread=False)
cs = firstDb.cursor()    # SqlLite için imleç oluşturma
cs.execute(
    """CREATE TABLE IF NOT EXISTS Users
  (
  "no" TEXT UNIQUE,
 "username"  TEXT UNIQUE,
 "password"  TEXT UNIQUE
 );"""
)


def record(ask=False):
    with sr.Microphone() as source:

        if ask:
            speak(ask)
        r.pause_threshold = 0.8
        audio = r.listen(source,  phrase_time_limit=2)
        voice = ''
        try:
            voice = r.recognize_google(audio, language='tr-TR')
        except sr.UnknownValueError:
            speak("tekrar edermisin")
        except sr.UnknownValueError:
            speak("sistem çalışmıyor")
        return voice


def response(voice):
    if 'panjurları aç' in voice:
        speak("Tamam senin için panjurları açıyorum.")
        try:
            cs.execute(""" SELECT * FROM Users """)
            firstipadress = cs.fetchall()
            eepromipadress = firstipadress[0][2]
            url_json = 'http://'+eepromipadress+'/manuel'
            print(eepromipadress)
            data = {'stepsize': '90'}
            headers = {'Content-Type': 'application/json; charset=UTF-8'}
            response, content = http.request(
                url_json, 'POST', headers=headers, body=json.dumps(data))

        except:
            if(http.timeout > 0.9):
                speak("Panjurlar bağlı gözükmüyor batuhan.")
    if 'panjurları kapat' in voice:
        speak("Tamam senin için panjurları kapatıyorum.")
        try:
            cs.execute(""" SELECT * FROM Users """)
            firstipadress = cs.fetchall()
            eepromipadress = firstipadress[0][2]
            url_json = 'http://'+eepromipadress+'/manuel'
            print(eepromipadress)
            data = {'stepsize': '0'}
            headers = {'Content-Type': 'application/json; charset=UTF-8'}
            response, content = http.request(
                url_json, 'POST', headers=headers, body=json.dumps(data))

        except:
            if(http.timeout > 0.9):
                speak("Panjurlar bağlı gözükmüyor batuhan.")

    if "saat kaç" in voice:
        speak(datetime.now().strftime('%H:%M:%S'))
    if 'arama yap' in voice:
        search = record("ne aramak istiyorsun")
        url = 'https://google.com/search?q='+search
        webbrowser.get().open(url)
        speak(search+'için bulduklarım')
    if 'tamamdır' in voice:
        speak('İyi Günler dilerim batuhan')
        exit()


def speak(string):

    tts = gTTS(string, lang='tr')
    rand = random.randint(1, 10000)
    file = 'auido-'+str(rand)+'.mp3'
    tts.save(file)
    playsound(file)
    os.remove(file)


speak("ne yapmak istiyorsun batuhan ")
time.sleep(1)
while(1):
    voice = record()
    print(voice)
    response(voice)

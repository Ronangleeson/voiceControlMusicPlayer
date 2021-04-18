import speech_recognition as sr
import csv
import sys
import simpleaudio as sa
import random
import pyaudio
import wave
import time
from pynput import keyboard
import os

playlist = list()
songCount = 0

from pynput.keyboard import Key, Controller

keyboardController = Controller()

def captureAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
    try:
        audioAsText = str(r.recognize_google(audio))
        print("Google Speech Recognition thinks you said: " + audioAsText)
        getCommand(audioAsText)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

# def start():   
#     text = "play"
#     getCommand(text)


def getCommand(audioAsText):
    audioAsText = audioAsText.lower()
    splitText = audioAsText.split()
    if (splitText[0] == "shuffle"):
        if len(splitText) == 1:
            shuffleLibrary()
        else:
            splitText.pop(0)
            splitText = ",".join(splitText)
            shuffleSelection(splitText)
        
    elif splitText[0] == "play":
        if len(splitText) == 1:
            playLibrary()
        else:
            splitText.pop(0) 
            splitText = ",".join(splitText)
            findSelection(splitText)
        
    else:
        print("Invalid command")


def findSelection(splitText):
    with open('musicDatabase.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for i in range(len(row)):
                if splitText == row[i]:
                    playlist.append(row[3])
        for i in playlist:
            if i != "filepath":
                playSong(i)

def playLibrary():
    with open('musicDatabase.csv', 'r') as file: 
        reader = csv.reader(file)
        for row in reader:
            if row[3] != 'filepath':
                playlist.append(row[3])
    for i in playlist:
            playSong(i)


def shuffleLibrary():
    with open('musicDatabase.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[3] != 'filepath':
                playlist.append(row[3])
    random.shuffle(playlist)
    for i in playlist:
        playSong(i)

def shuffleSelection(splitText):
    with open('musicDatabase.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            for i in range(len(row)):
                if splitText == row[i]:
                    playlist.append(row[3])
    random.shuffle(playlist)
    for i in playlist:
        if i != "filepath":
            playSong(i)

paused = False
def on_press(key):
    global paused
    global songCount

    print(key)
    if key == keyboard.Key.space:
        if stream.is_stopped():
            stream.start_stream()
            paused = False
            return False
        elif stream.is_active():
            stream.stop_stream()
            paused = True
            return False

    if key == keyboard.Key.right:
        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()
        try:
            songCount += 1
            playSong(playlist[songCount])
        except:
            print("end of playlist")
            os._exit(0)

    if key == keyboard.Key.left:
        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()
        if songCount == 0:
            playSong(playlist[0])
        else:
            songCount -= 1
            playSong(playlist[songCount])

    if key == keyboard.Key.up:
        keyboardController.press(Key.media_volume_up)
        keyboardController.release(Key.media_volume_up)
        
    if key == keyboard.Key.down:
        keyboardController.press(Key.media_volume_down)
        keyboardController.release(Key.media_volume_down)

    if key == keyboard.Key.enter:
        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()
        playlist.clear()
        songCount = 0
        captureAudio()

    return False


def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

def playSong(songPath):
    global songCount
    global wf
    global stream
    global p

    wf = wave.open(songPath, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active() or paused==True:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()

    songCount += 1


def main():
    # start()
    captureAudio()

main()

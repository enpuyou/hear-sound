#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import speech_recognition as sr

# obtain audio from the microphone
# TODO: customize pause time
r = sr.Recognizer()
r.pause_threshold = 0.2
r.non_speaking_duration = 0.1
r.energy_threshold = 1200
while True:
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Sphinx
    try:
        print("You said " + r.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))

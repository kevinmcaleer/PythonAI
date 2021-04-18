import pyaudio
import wave
import pyttsx3
import speech_recognition as sr
from webui import *

class AI():
    __name = ""
    __skills = []

    def __init__(self, name=None):
        self.engine = pyttsx3.init()
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        
        if name is not None:
            self.__name = name
        
        print("Listening")
        with self.m as source: 
            self.r.adjust_for_ambient_noise(source)
        
        # Launch Web UI
        # main()
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value
        sentence = "Hello, my name is" + self.__name
        self.engine.say(sentence)
        self.engine.runAndWait()

    def say(self, sentence):
        # self.engine("saying:", sentence)
        self.engine.say(sentence)
        self.engine.runAndWait()

    def listen(self):
        print("Say Something")
        with self.m as source: 
                audio = self.r.listen(source)
        print("Got it")
        phrase = self.r.recognize_google(audio)
        
        try:
            phrase = self.r.recognize_google(audio)
            if phrase == "robot":
                self.engine.say("Im listening")
                self.engine.runAndWait()
                with self.m as source: audio = self.r.listen(source)
                phrase = self.r.recognize_google(audio)
                
                print("you said" + self.r.recognize_google(audio))
                self.engine.say("You said " + self.r.recognize_google(audio))
                self.engine.runAndWait()
                return phrase 
        except LookupError:
            print("Could not understand audio")
        return ""

    def register_skill(self, newskill):
        self.__skills.append(newskill)
        print("added new skill", newskill.name)

    def list_skills(self):
        for skill in self.__skills:
            print(skill.name)

    
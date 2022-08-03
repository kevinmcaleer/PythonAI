import pyttsx3
import speech_recognition as sr 
from conversation_history import Conversation_history
from vosk import Model, KaldiRecognizer
from pyaudio import PyAudio, paInt16
import json

"""
pip install vosk
download the models from https://alphacephei.com/vosk/models
"""

class AI():
    __name = ""
    __skill = []
    __conversation_history = Conversation_history()

    def __init__(self, name=None):
        self.engine = pyttsx3.init()
        # self.engine.setProperty('voice', 'com.apple.speech.synthesis.voice.ava.premium')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice' ,voices[5].id)
        name = voices[5].name
        print(name)
        # voices = self.engine.getProperty('voices')
        # for voice in voices:
        #     print(voice, voice.id)
        # self.r = sr.Recognizer()
        model = Model('./model') # path to model
        self.r = KaldiRecognizer(model, 16000)
        # self.m = sr.Microphone() 
        self.m = PyAudio()

        if name is not None:
            self.__name = name 

       
        self.audio = self.m.open(format=paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        self.audio.start_stream()

        # print("calibratng microphone")
        # with self.m as source:
        #     self.r.adjust_for_ambient_noise(source)
        #     print("done calibrating")
    @property 
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        sentence = "Hello, my name is" + self.__name
        self.__name = value
        self.engine.say(sentence)
        self.engine.runAndWait()

    def say(self, sentence):
        print(sentence)
        self.__conversation_history.add_item(message_type='RESPONSE', message=sentence)
        self.engine.say(sentence)
        self.engine.runAndWait()

    def listen(self):
        # print("Say Something")
        heard_something = False
        audio = None
      
        phrase = ""

        if self.r.AcceptWaveform(self.audio.read(4096,exception_on_overflow = False)): 
            phrase = self.r.Result()
            phrase = str(json.loads(phrase)["text"])
            self.__conversation_history.add_item(message_type='COMMAND', message=phrase)
            return phrase   
        return None
    def get_conversation(self):
        return self.__conversation_history.get_items()
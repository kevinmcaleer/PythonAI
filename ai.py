import pyttsx3
from vosk import Model, KaldiRecognizer
from pyaudio import PyAudio, paInt16
import json
from eventhook import Event_hook

"""
pip install vosk
download the models from https://alphacephei.com/vosk/models
"""

class AI():
    __name = ""
    __skill = []
   
    def __init__(self, name=None):
        self.engine = pyttsx3.init()

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice' ,voices[5].id)
        name = voices[5].name
        print(name)

        model = Model('./model') # path to model
        self.r = KaldiRecognizer(model, 16000)

        self.m = PyAudio()

        if name is not None:
            self.__name = name 

        self.audio = self.m.open(format=paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
        self.audio.start_stream()

        # Setup event hooks
        self.before_speaking = Event_hook()
        self.after_speaking = Event_hook()
        self.before_listening = Event_hook()
        self.after_listening = Event_hook()
        
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
        self.before_speaking.trigger(sentence)
        self.engine.say(sentence)
        self.engine.runAndWait()
        self.after_speaking.trigger(sentence)

    def listen(self):
           
        phrase = ""
        
        if self.r.AcceptWaveform(self.audio.read(4096,exception_on_overflow = False)): 
            self.before_listening.trigger()
            phrase = self.r.Result()
            phrase = phrase.removeprefix('the')
            
            phrase = str(json.loads(phrase)["text"])

            if phrase:
                self.after_listening.trigger(phrase)
            return phrase   

        return None

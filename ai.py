import pyttsx3
from vosk import Model, KaldiRecognizer
from pyaudio import PyAudio, paInt16
import json
from eventhook import Event_hook
from threading import Thread, Lock

"""
pip install vosk
download the models from https://alphacephei.com/vosk/models
"""

class AI():
    __name = ""
    __skill = []
    lock = Lock()
   
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

    def speak(self, sentence):
        """ Added extra function so it can be can be called from a thread """
        
        # Lock the thread so it doesn't try to speak while it is already speaking
        self.lock.acquire()
        print(sentence)
        self.before_speaking.trigger(sentence)
        self.engine.say(sentence)
        self.engine.iterate()
        # self.engine.runAndWait()
        self.after_speaking.trigger(sentence)

        # Release the lock
        self.lock.release()


    def say(self, sentence):
        """ launch a new thread to speak """
        self.engine.startLoop(False)
        t = Thread(target = self.speak, args = (sentence,))
        t.start()
        self.engine.endLoop()
        # t.join()
        
    def listen(self):
           
        phrase = ""
        
        if self.r.AcceptWaveform(self.audio.read(4096,exception_on_overflow = False)): 
            self.before_listening.trigger()
            phrase = self.r.Result()
            phrase = phrase.removeprefix('the ')
            
            phrase = str(json.loads(phrase)["text"])

            if phrase:
                self.after_listening.trigger(phrase)
            return phrase   

        return None

    def stop_ai(self):
        self.engine.stop()
        print("stopped engine")

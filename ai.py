import pyttsx3
import speech_recognition as sr 

class AI():
    __name = ""
    __skill = []

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
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
       

        if name is not None:
            self.__name = name 

        print("Listening")
        with self.m as source:
            self.r.adjust_for_ambient_noise(source)

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
        self.engine.say(sentence)
        self.engine.runAndWait()

    def listen(self):
        print("Say Something")
        with self.m as source:
            try:
                audio = self.r.listen(source)
            except:
                pass
        # print("got it")
        phrase = ""
        try:
            phrase = self.r.recognize_google(audio, show_all=False, language="en_US")
            phrase = str(phrase)
            # sentence = "Got it, you said" + phrase
            # self.engine.say(sentence)
            # self.engine.runAndWait()
        except:
            pass
            # print("Sorry, didn't catch that")
            # self.engine.say("Sorry didn't catch that")
            # self.engine.runAndWait()
        print("You Said", phrase)
        return phrase
    

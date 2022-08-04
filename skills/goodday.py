# skills extension
from dataclasses import dataclass
from skills import factory
from datetime import datetime
from ai import AI

@dataclass
class GooddaySkill:
    name = 'goodday'

    def commands(self, command:str):
        return ['goodday', 'good day', 'good evening', 'good night']

    def handle_command(self, command:str, ai:AI):
        now = datetime.now()
        hr = now.hour
        if hr <= 0 <=12:
            message = "Morning"
        if hr >=12 <= 17:
            message = "Afternoon"
        if hr >=17 <=21:
            message = "Evening"
        if hr > 21: message = "Night"

        message = "Good " + message + " Kevin"
        ai.say(message)
        return 'goodday'

def initialize():
    factory.register('goodday_skill', GooddaySkill)
    # print("goodday initialized")
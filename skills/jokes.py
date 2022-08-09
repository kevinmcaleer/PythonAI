from dataclasses import dataclass
from skills import factory
from ai import AI
import pyjokes
    
@dataclass
class Jokes_skill():
    name = 'jokes_skill'

    def commands(self, command:str):
        return ['tell me a joke','make me laugh', 'joke']

    def handle_command(self, command:str, ai:AI):
        joke = pyjokes.get_joke()
        ai.say(joke)
        return joke

def initialize():
    factory.register('jokes_skill', Jokes_skill)

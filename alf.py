from ai import AI
from skill_weather import Skill_weather
from skill_jokes import Skill_Jokes
import pyjokes

alf = AI()

# alf.name = "Robbie the Robot"

def joke():
    # alf.say("I'm a Robot not a commedian")
    funny = pyjokes.get_joke()
    print(funny)
    alf.say(funny)

weather = Skill_weather()
jokes = Skill_Jokes()
alf.register_skill(weather)
alf.register_skill(jokes)
alf.list_skills()

command = ""
while True and command != "goodbye":
    command = alf.listen()
    print("command was:",command)

    if command == "tell me a joke":
        joke()
    # do commands

alf.say("Good bye, I'm going to sleep now")
import pyjokes
from ai import AI


alf = AI()

def joke():
    funny = pyjokes.get_joke()
    print(funny)
    alf.say(funny)

command = ""
while True and command != "goodbye":
    command = alf.listen()
    print("command was:", command)

    if command == "tell me a joke":
        joke()
    
alf.say("Goodbye, I'm going to sleep now")
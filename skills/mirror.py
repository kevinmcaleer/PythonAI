from dataclasses import dataclass
from skills import factory
from ai import AI

@dataclass
class Mirror_mirror_skill():
    name = "mirror_mirror_skill"

    def commands(self, command:str):
        return ["mirror", "mirror mirror on the wall", "mirror mirror on the wall, who's the fairest one of all?"]

    def handle_command(self, command:str, ai:AI):
        message = "You are the most beautiful person, inside and out."
        ai.say(message)
        return message

def initialize():
    factory.register("mirror_mirror_skill", Mirror_mirror_skill)

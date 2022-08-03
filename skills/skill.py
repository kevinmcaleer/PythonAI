from typing import Protocol
from ai import AI

class Skill(Protocol):

    def commands(self, command:str):
        """ Return a list of commands that this skill can handle """
        pass
    
    def handle_command(self, command:str, ai:AI):
        """ Handle a command """
        pass


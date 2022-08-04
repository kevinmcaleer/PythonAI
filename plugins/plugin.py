from typing import Protocol
from ai import AI

class Plugin(Protocol):
    
    def handle_command(self, command:str, ai:AI):
        """ Handle a command """
        pass

    def register(self):
        ...
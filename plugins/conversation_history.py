# Conversation History
# Kevin McAleer
# July 2022

from time import strftime, localtime
from dataclasses import dataclass
from ai import AI
import plugins.plugin_factory

class Conversation_history:
    items = []
    history: int = 20

    def __init__(self):
        self.items = []

    def add_item(self, message_type:str, message:str):
        """ Add items into the conversation history """

        # Guard statement
        if message_type not in ['RESPONSE', 'COMMAND']:
            print("Invalid message type")
            return

        item = {'message_type': message_type, 'message': message, 'time': strftime("%Y-%m-%d %H:%M:%S", localtime())}
        self.items.append(item)
        if len(self.items) > self.history:
            self.items.pop(0)
        
    def get_items(self)->list:
        """ Get the items from the conversation history """
        return self.items
    
    def get_items_by_type(self, message_type:str)->list:
        """ Get the items from the conversation history """
        return [item for item in self.items if item['message_type'] == message_type]
    
    def __len__(self):
        """ Returns the number of items in the Conversation History """
        return len(self.items)
    

@dataclass
class Conversation_history_plugin:
    name = 'conversation_history'
    __conversation_history = Conversation_history()

    def add_response(self, message):
        self.__conversation_history.add_item(message_type='RESPONSE', message=message)
        return self

    def add_command(self, message):
        self.__conversation_history.add_item(message_type='COMMAND', message=message)
        return self

    def register(self, ai:AI):
        self.ai = ai
        
        self.ai.after_speaking.register(self.add_response)
        self.ai.after_listening.register(self.add_command) 
        return self

def initialize():
    # register with Factory or plugin?
    plugins.plugin_factory.register('conversation_history_plugin', Conversation_history_plugin)

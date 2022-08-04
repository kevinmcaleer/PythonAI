# Conversation History
# Kevin McAleer
# July 2022

from time import strftime, localtime
from dataclasses import dataclass
from ai import AI
import plugins.plugin_factory
from flask import Flask
from flask_cors import CORS
import logging
from threading import Thread

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
    app = None

    __conversation_history = Conversation_history()
    def __init__(self):
        self.app = Flask(__name__)
        CORS(self.app)

    def add_response(self, message):
        self.__conversation_history.add_item(message_type='RESPONSE', message=message)
        return self

    def add_command(self, message):
        self.__conversation_history.add_item(message_type='COMMAND', message=message)
        return self

    def get_history(self):
        return self.__conversation_history.get_items()

    def start_flask_thread(self):
        """ Start flask thread """
        print("starting api thread")
        self.app.add_url_rule('/api', 'conversation_history', self.get_history)
        self.app.run(debug=False, host='0.0.0.0', port=2222)
        self.app.logger.setLevel(logging.ERROR)

    def start(self):
        print("starting API server")
        self.flask = Thread(target=self.start_flask_thread,args=())
        self.flask.start()
        return self

    def stop(self):
        # shutdown the flask server
        print("stopping api server")
        self.flask.join()

    def register(self, ai:AI):
        self.ai = ai
        self.ai.after_speaking.register(self.add_response)
        self.ai.after_listening.register(self.add_command) 
        self.ai.start.register(self.start)  
        self.ai.stop.register(self.stop)
        return self

def initialize():
    # register with Factory or plugin?
    plugins.plugin_factory.register('conversation_history_plugin', Conversation_history_plugin)

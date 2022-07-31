# Conversation History
# Kevin McAleer
# July 2022

from time import strftime, localtime

class Conversation_history:
    items = []
    
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
        
    def get_items(self)->list:
        """ Get the items from the conversation history """
        return self.items
    
    def get_items_by_type(self, message_type:str)->list:
        """ Get the items from the conversation history """
        return [item for item in self.items if item['message_type'] == message_type]

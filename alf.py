import pyjokes
from ai import AI
from todo import Todo, Item
from weather import Weather
from randfacts import randfacts
from datetime import datetime

alf = AI()
todo = Todo()
# item = Item(title="get shopping")
# item2 = Item("potatoes")
# todo.new_item(item)
# todo.new_item(item2)

def fact():
    fun_fact = randfacts.get_fact()
    print(fun_fact)
    alf.say(fun_fact)

def joke():
    funny = pyjokes.get_joke()
    print(funny)
    alf.say(funny)

def add_todo()->bool:
    item = Item()
    alf.say("Tell me what to add to the list")
    try:
        item.title = alf.listen()
        todo.new_item(item)
        message = "Added " + item.title
        alf.say(message)
        return True
    except:
        print("oops there was an error")
        return False
    
def list_todos():
    if len(todo) > 0:
        alf.say("Here are your to do's")
        for item in todo:
            alf.say(item.title)
    else:
        alf.say("The list is empty!")

def remove_todo()->bool:
    alf.say("Tell me which item to remove")
    try:
        item_title = alf.listen()
        todo.remove_item(title=item_title)
        message = "Removed " + item_title
        alf.say(message)
        return True
    except:
        print("opps there was an error")
        return False
    
def weather()->bool:
    """ Gets the weather or returns an error """
    try:
        myweather= Weather()
        forecast = myweather.forecast
        print(forecast)
        alf.say(forecast)
        return True
    except:
        print("there was an error with the weather")
        return False

command = ""
alf.say("Hello")
while True and command != "goodbye":
    try:
        command = alf.listen()
        command = command.lower()
    except:
        print("oops there was an error")
        command = ""
    print("command was:", command)

    if command == "tell me a joke":
        joke()
        command = ""
    if command in ["add to-do","add to do", "add item"]:
        add_todo()
        command = ""
    if command in ["list todos", "list todo", "list to do", "list to-do", "list to do's",'list items']:
        list_todos()
        command = ""
    if command in ["remove todo", "remove item", "mark done", "remove todos", "remove to-do", "remove to do's"]:
        remove_todo()
    if command in ["what's the weather like", "Weather", "what's the forecast", "what's the weather today"]:
        weather()
    if command in ["tell me something","tell me a fact", "tell me a random fact","another one"]:
        fact()
    if command in ["good morning","good afternoon","hey alf","good afternoon","good evening","good night"]:
      
        now = datetime.now()
        # time = datetime.strftime(now, "%Y-%m-%d %H:%M:%S")
        hr = now.hour
        if hr <= 0 <= 12: 
            message = "Morning"
        if hr >= 12 <= 17:
            message = "Afternoon"
        if hr > 17 <= 21:
            message = "Evening"
        if hr >21: message = "Night"
        message = "Good " + message + "Kevin."
        alf.say(message)
        weather()
        fact()
        list_todos()
        joke()
alf.say("Goodbye!")
import pyjokes
from ai import AI
from todo import Todo, Item
from weather import Weather
from randfacts import randfacts
from datetime import datetime
from calendar_skill import Calendar_skill
import dateparser

alf = AI()
todo = Todo()
calendar = Calendar_skill()
calendar.load()

def facts():
    fact = randfacts.get_fact()
    # print(fact)
    alf.say(fact)

def joke():
    funny = pyjokes.get_joke()
    # print(funny)
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
        alf.say("The to do list is empty!")

def weather():
    myweather = Weather()
    forecast = myweather.forecast
    # print(forecast)
    alf.say(forecast)

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
    
def add_event()->bool:
    alf.say("What is the name of the event")
    try:
        event_name = alf.listen()
        alf.say("When is this event?")
        event_begin = alf.listen()
        event_isodate = dateparser.parse(event_begin).strftime("%Y-%m-%d %H:%M:%S")
        alf.say("What is the event description?")
        event_description = alf.listen()
        message = "Ok, adding event " + event_name
        alf.say(message)
        calendar.add_event(begin=event_isodate, name=event_name, description=event_description)
        calendar.save()
        return True
    except:
        print("opps there was an error")
        return False
def remove_event()->bool:
    alf.say("What is the name of the event you want to remove?")
    try:
        event_name = alf.listen()
        try:
            calendar.remove_event(event_name=event_name)
            alf.say("Event removed successfully")
            calendar.save()
            return True
        except:
            alf.say("Sorry I could not find the event",event_name)
            return False
    except:
        print("opps there was an error")
        return False

def list_events(period):
    this_period = calendar.list_events(period=period)
    if this_period is not None:
        message = "There "
        if len(this_period) > 1:
            message = message + 'are '
        else:
            message = message + 'is '
        message = message + str(len(this_period)) 
        if len(this_period) > 1:
            message = message + ' events'
        else:
            message = message + ' event'
        message = message + " in the diary"
        # print(message)
        alf.say(message)
        for event in this_period:
            event_date = event.begin.datetime
            weekday = datetime.strftime(event_date, "%A")
            day = str(event.begin.datetime.day)
            month = datetime.strftime(event_date, "%B")
            year = datetime.strftime(event_date, "%Y")
            time = datetime.strftime(event_date, "%I:%M %p")
            name = event.name
            description = event.description
            message = "On " + weekday + " " + day + " of " + month + " " + year + " at " + time    
            message = message + ", there is an event called " + name
            message = message + " with an event description of " + description
            # print(message)
            alf.say(message)

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
    if command in ['what is the weather like', 'give me the forecast',"what's the weather"]:
        weather()
    if command in ['tell me a fact','tell me something']:
        facts()
    if command in ['good morning','good evening','good night','good afternoon']:
        now = datetime.now()
        hr = now.hour
        if hr <= 0 <=12:
            message = "Morning"
        if hr >=12 <= 17:
            message = "Afternoon"
        if hr >=17 <=21:
            message = "Evening"
        if hr > 21: message = "Night"

        message = "Good " + message + " Kevin"
        alf.say(message)
        list_events(period="this week")
        weather()
        list_todos()
        joke()
        facts()
    
    # Calendar
    if command in ['add event','add to calendar','new event','add a new event']:
        add_event()
    if command in ['delete event','remove event','cancel event']:
        remove_event()
    if command in ['list events',"what's on this month","what's coming up this month"]:
        list_events(period='this month')
    if command in ["what's on this week","what's coming up this week","what's happening"]:
        list_events(period='this week')
    if command in ['list all events']:
        list_events(period='all')
  
alf.say("Goodbye!")
from ai import AI
from datetime import datetime
# from calendar_skill import Calendar_skill
# import dateparser 
from skills import factory, loader
import json

alf = AI()

# calendar = Calendar_skill()
# calendar.load()

    
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

# register the skills
# factory.register('hello_world', Hello_skill)
# factory.register('weather_skill', Weather_skill)

with open("./skills/skills.json") as f:
    data = json.load(f)

    # load the plugins
    loader.load_skills(data["plugins"])
print(data["skills"])
skills = [factory.create(item) for item in data["skills"]]
print(f'skills: {skills}')


alf.say("Hello")
while True and command != "good bye":
    command = ""
    command = alf.listen()
    if command:
        command = command.lower()
        print(f'command heard: {command}') 
        for skill in skills:
            if command in skill.commands(command):
                skill.handle_command(command, alf)
    
    ################################## 
    # Refactor all the code below

    
    # Calendar
    # if command in ['add event','add to calendar','new event','add a new event']:
    #     add_event()
    # if command in ['delete event','remove event','cancel event']:
    #     remove_event()
    # if command in ['list events',"what's on this month","what's coming up this month"]:
    #     list_events(period='this month')
    # if command in ["what's on this week","what's coming up this week","what's happening"]:
    #     list_events(period='this week')
    # if command in ['list all events']:
    #     list_events(period='all')
  
alf.say("Goodbye!")
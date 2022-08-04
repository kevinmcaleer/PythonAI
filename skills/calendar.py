# Calendar_skill.py
# AI Calendar skill
# Kevin McAleer - August 2021

from ics import Calendar, Event
from pathlib import Path
import os
import yaml
from datetime import datetime
from dateutil.relativedelta import *
import pytz
from dataclasses import dataclass
import dateparser
from skills import factory
from ai import AI

calendar_filename = 'docs/myfile.ics'
calendar_datafile = 'myfile.yml'

class Calendar_for_AI():
    c = Calendar()
    
    def add_event(self, begin:str, name:str, description:str=None)-> bool:
        ''' adds an event to the calendar '''
        e = Event()
        e.name = name
        e.begin = begin # format should be - '2021-08-16 16:28:00'
        e.description = description
        try:
            self.c.events.add(e)
            return True
        except:
            print("there was a problem adding the event, sorry.")
            return False

    def remove_event(self, event_name:str):
        ''' Removes the event from the calendar '''
        
        # find the event
        for event in self.c.events:
            if event.name == event_name:
                # found it
                self.c.events.remove(event)
                print("removing event:",event_name)
                return True
        
        # not found
        print("Sorry Could not find that event:",event_name)
        return False
                
    def parse_to_dict(self):
        dict = []
        for event in self.c.events:
            my_event = {}
            my_event['begin'] = event.begin.datetime
            my_event['name'] = event.name
            my_event['description'] = event.description
            dict.append(my_event)
            # print('parsing file:', yaml.dump(dict, default_flow_style=False))
        return dict

    def save(self):
        # Save the Calendar ICS file
        with open(calendar_filename,'w') as my_file:
            my_file.writelines(self.c)
        # Save the YAML Data file

        # first check that there are some entries in the dictionary, otherwise remove the file
        if self.c.events == set():
            print ("No Events - Removing YAML file")
            try:
                os.remove(calendar_datafile)
            except:
                print("oops couldn't delete the YAML file")
        else:
            with open(calendar_datafile,'w') as outfile:
                
                yaml.dump(self.parse_to_dict(), outfile, default_flow_style=False)

    def load(self):
        ''' load the Calendar data from the YAML file '''
        filename = calendar_datafile
        my_file = Path(filename)

        # check if the file exists
        if my_file.is_file():
            stream = open(filename,'r')
            events_list = yaml.load(stream)
            for item in events_list:
                e = Event()
                e.begin = item['begin']
                e.description = item['description']
                e.name = item['name']
                self.c.events.add(e)
        else:
            # file doesnt exist
            print("file does not exist")

    def list_events(self,period:str=None)->bool:
        ''' Lists the upcoming events 
            if `period` is left empty it will default to today
            other options are:
            `all` - lists all events in the calendar
            `this week` - lists all the events this week
            `this month` - lists all the events this month
        '''

        if period == None:
            period = "this week"

        # check that there are events
        if self.c.events == set():
            # no events found
            print("No Events In Calendar")
            return False
        else:
            event_list = []
            # have to fix the localisation - thats the +00 timezone bit on the date
            # otherwise it complains of non-naive date being compared with naive date
            now = pytz.utc.localize(datetime.now())
            if period == "this week":
                nextperiod = now+relativedelta(weeks=+1)
            if period == "this month":
                nextperiod = now+relativedelta(months=+1)
            if period == "all":
                nextperiod = now+relativedelta(years=+100)
            for event in self.c.events:
                event_date = event.begin.datetime
                if (event_date >= now) and (event_date <= nextperiod):    
                    event_list.append(event)
            return event_list


@dataclass
class Calender_skill():
    name = 'calendar_skill'
    calendar = Calendar_for_AI()
    calendar.load()

    def commands(self, command:str):
        return ['add event','add to calendar','new event','add a new event',
                'delete event','remove event','cancel event',
                'list events',"what's on this month","what's coming up this month",
                "what's on this week","what's coming up this week","what's happening",
                'list all events']
    
    def add_event(self, alf:AI)->bool:
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
            self.calendar.add_event(begin=event_isodate, name=event_name, description=event_description)
            self.calendar.save()
            return True
        except:
            print("opps there was an error")
            return False
    def remove_event(self, alf:AI)->bool:
        alf.say("What is the name of the event you want to remove?")
        try:
            event_name = alf.listen()
            try:
                self.calendar.remove_event(event_name=event_name)
                alf.say("Event removed successfully")
                self.calendar.save()
                return True
            except:
                alf.say("Sorry I could not find the event",event_name)
                return False
        except:
            print("opps there was an error")
            return False

    def list_events(self, period, alf:AI)->bool:
        this_period = self.calendar.list_events(period=period)
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
       
    def handle_command(self, command:str, ai:AI):
        
        if command in ['add event','add to calendar','new event','add a new event']:
            self.add_event()
        if command in ['delete event','remove event','cancel event']:
            self.remove_event()
        if command in ['list events',"what's on this month","what's coming up this month"]:
            self.list_events(period='this month')
        if command in ["what's on this week","what's coming up this week","what's happening"]:
            self.list_events(period='this week')
        if command in ['list all events']:
            self.list_events(period='all', ai=ai)

def initialize():
    factory.register('calendar_skill', Calender_skill)

from dataclasses import dataclass
from skills import factory
from ai import AI
import time
import threading

class CountDownTimer():
    hours = 0
    minutes = 0
    seconds = 0
    # duration = 25 # minutes default
    # duration_in_seconds = duration * 60
    duration_in_seconds = 10 # for testing
    alarm = False
    
    def __init__(self):
        
        self.start_time = time.time()
        print(f'start time is :{self.start_time}')
    
    @property
    def duration(self):
        return self.duration_in_seconds * 60
    
    @duration.setter
    def duration(self, duration_in_minutes):
        self.duration_in_seconds = duration_in_minutes * 60
            
    @duration.setter
    def duration_seconds(self, duration):
        self.target_time = time.time() + duration
        self.duration_in_seconds = duration
            
    def reset(self):
        self.start_time = time.time()
        self.alarm = False
    
    def time_to_str(self,time_as_number)->str:
        target = time.localtime(time_as_number)
        hours =  target[3]
        minutes = target[4]
        seconds =  target[5]
        return f'{hours:02}:{minutes:02}:{seconds:02}'
    
    @property
    def start_time_str(self)->str:
        target = self.start_time

        return self.time_to_str(target)
    
    @property
    def target_time(self)->int:
        # add duration in seconds to epoc
        target = self.start_time + (self.duration_in_seconds)
        return target
    
    @property
    def target_str(self)->str:
        """ Return the target time as a string """

        return self.time_to_str(self.target_time)
    
    @property
    def remaining_str(self)->str:
        """ Return the remaining time as a string """
        time_left = self.remaining_seconds       

        return self.time_to_str(time_left)
    
    @property
    def current_time_str(self)->str:
        current = time.time()

        return self.time_to_str(current)
    
    @property
    def remaining_seconds(self)->int:
        """ returns remaining seconds """
        
        remaining = self.target_time - time.time()
#         print(f' remaining = {remaining}')
        if remaining > 0:
            
            return remaining
        else: return 0
    
    def isalarm(self):
        if self.remaining_seconds == 0:
            self.alarm = True
            return True
        else:
            return False
    
    def tick(self):
        
        # Get time as tuple
        # (year, month, mday, hour, minute, second, weekday, yearday)
       
        return self.remaining_str
    
    def status(self):
        
        if not self.isalarm():
            print(f'Start time    : {self.start_time_str}', end='')
            print(f' | Current time  : {self.current_time_str}', end='')
            print(f' | Target time   : {self.target_str}', end='')
            print(f' | Remaining time: {self.remaining_str}')

@dataclass
class Pomodoro_skill():
    name = "pomodoro_skill"

    def __init__(self):
        self.pomodoro = CountDownTimer()

    def commands(self, command:str):
        return ["set timer", "start pomodoro", "pomodoro, how long left", "how long is left"]

    def countdown(self,ai):
        while not self.pomodoro.isalarm():
            time.sleep(0.5)
        message = "The Pomodoro timer has finished"
        ai.say(message)

    def handle_command(self, command:str, ai:AI):
        message = ''
        if command == "set timer":
            self.pomodoro.reset()
            message = "Countdown started, I'll let you know when it's done"
            thread = threading.Thread(target=self.countdown,args=(ai,))
            thread.start()
        ai.say(message)
        # thread.join()
        return message

def initialize():
    factory.register("pomodoro_skill", Pomodoro_skill)
    print('Pomodoro skill loaded')

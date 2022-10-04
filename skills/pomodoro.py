from dataclasses import dataclass
from skills import factory
from ai import AI
import time
import threading
from simple-countdowntimer import CountdownTimer

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

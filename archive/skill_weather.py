# Weather skill

from skills import Skill
from pyowm import OWM
from datetime import datetime

location = 'Bolton, GB'
api_key = '3937f2958349fd1ad4e3704fa0b0d24e'

class Skill_weather(Skill):
    
    def __init__(self):
        self.name = "Weather"
        self.version = 1.0
        self.actions = ['get_weather']    
        self.ow = OWM(api_key)
        self.mgr = self.ow.weather_manager()
        self.actions = ["get weather"]
        
    def weather(self):
        forecast = self.mgr.weather_at_place(location)
        return forecast

    def execute(self, action):
        if action in [self.actions]:
            if action == "get weather":
                self.weather()

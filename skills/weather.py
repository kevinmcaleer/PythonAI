# Weather.py
# AI Weather skill
# Kevin McAleer - July 2021

from pyowm import OWM
from geopy import Nominatim, location
from datetime import datetime

from dataclasses import dataclass
from skills import factory
from ai import AI

class Weather():

    # The location of where you want the forecast for
    __location = "Bolton, GB"

    # API Key
    api_key = "90be93527babd2a823f16c364325e6d1"

    def __init__(self):
        self.ow = OWM(self.api_key)
        self.mgr = self.ow.weather_manager()
        locator = Nominatim(user_agent="myGeocoder")
        city = "Bolton"
        country = "GB"
        self.__location = city + ", " + country
        loc = locator.geocode(self.__location)
        self.lat = loc.latitude
        self.long = loc.longitude

    def uv_index(self, uvi:float):
        """ Returns a message depending on the UV Index provided """
        message = ""
        if uvi <= 2.0:
            message = "The Ultraviolet level is low, no protection is required."
        if uvi >= 3.0 and uvi <6.0:
            message = "The Ultraviolet level is medium, skin protection is required."
        if uvi >= 6.0 and uvi <8.0:
            message = "The Ultraviolet level is high, skin protection is required."
        if uvi >= 8.0 and uvi <11.0:
            message = "The Ultraviolet level is very high, extra skin protection is required."
        if uvi >= 11.0:
            message = "The Ultraviolet level is extremely high, caution is advised and extra skin protection is required."
        return message

    @property
    def weather(self):
        forecast = self.mgr.one_call(lat=self.lat, lon=self.long)
        return forecast

    @property
    def forecast(self):
        """ Returns the forecast at this location """

        forecast = self.mgr.one_call(lat=self.lat, lon=self.long)
        detail_status = forecast.forecast_daily[0].detailed_status
        pressure = str(forecast.forecast_daily[0].pressure.get('press'))
        humidity = str(forecast.forecast_daily[0].humidity)
        sunrise = datetime.utcfromtimestamp(forecast.forecast_daily[0].sunrise_time()).strftime("%H:%M:%S")
        sunset = datetime.utcfromtimestamp(forecast.forecast_daily[0].sunset_time()).strftime("%H:%M:%S")
        temperature = str(forecast.forecast_daily[0].temperature('celsius').get('day'))
        uvi = forecast.forecast_daily[0].uvi

        # print('detailed status: ', detail_status)
        # print("humidity ", humidity)
        # print("pressure ", pressure)
        # print("sunrise: ", sunrise)
        # print("Sunset ", sunset)
        # print("temperature", temperature)
        # print("UVI ", uvi)
        
        message = "Here is the Weather: Today will be mostly " + detail_status \
                + ", humidity of " + humidity + " percent" \
                + " and a pressure of " + pressure + " millibars" \
                + ". The temperature is " + temperature + "degrees " \
                + ". Sunrise was at " + sunrise \
                + " and sunset is at " + sunset \
                + ". " + self.uv_index(uvi)

        # print(message)
        return message



@dataclass
class Weather_skill:
    name = 'weather_skill'

    def commands(self, command:str):
        return ['weather', 'forecast', 'what is the weather like', 'give me the forecast',"what's the weather","what's the weather like"]

    def handle_command(self, command:str, ai:AI):
        myweather = Weather()
        forecast = myweather.forecast
        ai.say(forecast)
        return forecast

def initialize():
    factory.register('weather_skill', Weather_skill)
    # print("Weather initialized")
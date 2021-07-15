# Weather skill

from pyowm import OWM
from geopy import Nominatim, geocoders
import geopandas
from datetime import datetime

class Weather():
    
    # The location of where you want the weather forecast for
    __location = 'Bolton, GB'

    # Replace this with your own API key
    api_key = '3937f2958349fd1ad4e3704fa0b0d24e'

    def __init__(self):
        self.ow = OWM(self.api_key)
        self.mgr = self.ow.weather_manager()
        locator = Nominatim(user_agent="myGeocoder")
        city = "Bolton"
        country = "GB"
        self.__location = city + ' ' + country
        loc = locator.geocode(self.__location)
        self.lat = loc.latitude
        self.long = loc.longitude

    @property    
    def weather(self):
        """ Returns the current weather at this location """
        forecast = self.mgr.one_call(lat=self.lat, lon=self.long)
        return forecast

    @property
    def forecast(self):
        """ Returns the forecast at this location 
        
        AI will say:
        
        Today will be mostly <detailed_status>, with a temperature of , and it will feel like <feels_like>, humidity is, and pressure is
        sunrise is at , and sunset is at 
        Tomorrow
        
        """
        forecast = self.mgr.one_call(lat=self.lat, lon=self.long)
        detailed_status = forecast.forecast_daily[0].detailed_status
        pressure = str(forecast.forecast_daily[0].pressure.get('press'))
        humidity = str(forecast.forecast_daily[0].humidity)
        # print(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
        sunrise = datetime.utcfromtimestamp(forecast.forecast_daily[0].sunrise_time()).strftime('%H:%M:%S')
        temperature = str(forecast.forecast_daily[0].temperature('celsius').get('day'))
        temp_high = str(forecast.forecast_daily[0].temperature('celsius').get('temp_min'))
        temp_low = str(forecast.forecast_daily[0].temperature('celsius').get('temp_max'))
        sunset = datetime.utcfromtimestamp(forecast.forecast_daily[0].sunset_time()).strftime('%H:%M:%S')
        feels_like = str(forecast.forecast_daily[0].temperature('celsius').get('feels_like_day'))

        # print('detailed status:',detailed_status)
        # print('humidity',humidity)
        print('temperature',temperature)
        # print('sunrise',sunrise)
        # print('sunset',sunset)
        # print('feels_like',feels_like)
        # print('pressure',pressure)

    # + ", with a high of " + temp_high + " and a low of " + temp_low \

        message = "Today will be mostly " + detailed_status \
                + ", with a temperature of  " + temperature \
                + ", humidity of " + humidity + " percent" \
                + " and a pressure of " + pressure + " millibars" \
                + ". Sunrise was at " + sunrise \
                + ", and Sunset at " + sunset
        return message

    @property
    def location(self):
        """ Returns the currently set location """
        return self.__location

    @location.setter
    def location(self, value):
        """ Sets the current location """
        self.__location = value

# Demo
# myweather= Weather()
# print(myweather.forecast)
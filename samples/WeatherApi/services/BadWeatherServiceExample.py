import requests

from samples.WeatherApi.logger.Logger import Logger, getStdOutLogHandler
from samples.WeatherApi.mappers.GeolocationMappers import GeolocationMappers
from samples.WeatherApi.mappers.WeatherMappers import WeatherMappers
from samples.WeatherApi.models.Weather import Weather
from samples.WeatherApi.services.IWeatherService import IWeatherService


class BadWeatherServiceExample(IWeatherService):
    def __init__(self):
        self.__log = Logger(__name__, 0,[getStdOutLogHandler()])
        self.__geolocationMapper = GeolocationMappers()
        self.__weatherMapper = WeatherMappers()

    def getCurrentWeather(self, city: str, code: str, country: str) -> Weather or None:
        key = "b4ee712c33e4cd9e785d8bbf032b1652"
        p = {'q': f'{city},{code},{country}', 'limit': 1, 'appid': key}
        r = requests.get("http://api.openweathermap.org/geo/1.0/direct", params=p)

        try:
            loc = self.__geolocationMapper.mapJsonToGeolocation(r.json()[0])
            p = {'lat': loc.latitude, 'lon': loc.longitude, 'appid': key}
            r = requests.get("http://api.openweathermap.org/data/2.5/weather", params=p)
            return self.__weatherMapper.mapJsonToWeather(r.json())
        except Exception as error:
            self.__log.error(f"{error}")
            return None

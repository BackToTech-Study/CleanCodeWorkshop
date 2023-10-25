from typing import Callable

import requests
from injector import inject

from samples.WeatherApi.logger.Logger import Logger
from samples.WeatherApi.configurations.WeatherServerConfiguration import WeatherServerConfiguration
from samples.WeatherApi.helpers.HttpHelpers import isNotPositiveResponse
from samples.WeatherApi.mappers.GeolocationMappers import GeolocationMappers
from samples.WeatherApi.mappers.WeatherMappers import WeatherMappers
from samples.WeatherApi.models.Geolocation import Geolocation
from samples.WeatherApi.models.Weather import Weather
from samples.WeatherApi.services.IWeatherService import IWeatherService


class WeatherService(IWeatherService):
    @inject
    def __init__(self,
                 weatherConfiguration: WeatherServerConfiguration,
                 geolocationMapper: GeolocationMappers,
                 weatherMapper: WeatherMappers,
                 logger: Logger):
        self.__apiKey = weatherConfiguration.ApiKey
        self.__geoLocationUrl = weatherConfiguration.BaseUrl+weatherConfiguration.GeoLocationEndpoint
        self.__dataUrl = weatherConfiguration.BaseUrl+weatherConfiguration.DataEndpoint
        self.__units = weatherConfiguration.Units
        self.__geolocationMapper = geolocationMapper
        self.__weatherMapper = weatherMapper
        self.__logger = logger

    def getGeolocation(self, city: str, stateCode: str, countryCode: str) -> Geolocation or None:
        parameters = {'q': f'{city},{stateCode},{countryCode}', 'limit': 1, 'units': self.__units, 'appid': self.__apiKey}
        result = requests.get(self.__geoLocationUrl, params=parameters)

        if result is None or isNotPositiveResponse(result.status_code):
            return None

        try:
            data = result.json()
            if data is None or len(data) == 0:
                self.__logger.info(f"No geolocation data for: {city},{stateCode},{countryCode}")
                return None
            return self.__geolocationMapper.mapJsonToGeolocation(data[0])
        except KeyError as error:
            self.__logger.error(f"Missing key in geolocation data for {city},{stateCode},{countryCode}: {error}")
            return None
        except Exception as error:
            self.__logger.error(f"Unexpected geolocation data for {city},{stateCode},{countryCode}: {error}")
            return None

    def getCurrentWeather(self, city: str, stateCode: str, countryCode: str) -> Weather or None:
        location: Geolocation = self.getGeolocation(city, stateCode, countryCode)
        if location is None:
            return None
        parameters = {'lat': location.latitude, 'lon': location.longitude, 'units': self.__units,  'appid': self.__apiKey}
        result = requests.get(self.__dataUrl, params=parameters)

        if result is None or isNotPositiveResponse(result.status_code):
            return None

        try:
            data = result.json()
            return self.__weatherMapper.mapJsonToWeather(data)
        except KeyError as error:
            self.__logger.error(f"Missing key in weather data for {city},{stateCode},{countryCode}: {error}")
            return None
        except Exception as error:
            self.__logger.error(f"Unexpected weather data for {city},{stateCode},{countryCode}: {error}")
            return None

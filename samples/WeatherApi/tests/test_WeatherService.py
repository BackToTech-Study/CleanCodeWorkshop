import unittest

from samples.WeatherApi.configurations.IConfigurationFactory import IConfigurationFactory
from samples.WeatherApi.configurations.JsonConfigurationFactory import JsonConfigurationFactory
from samples.WeatherApi.configurations.LoggerConfiguration import LoggerConfiguration
from samples.WeatherApi.configurations.WeatherServerConfiguration import WeatherServerConfiguration
from samples.WeatherApi.logger.Logger import Logger, getStdOutLogHandler
from samples.WeatherApi.configurations.Dynamic import Dynamic
from samples.WeatherApi.mappers.GeolocationMappers import GeolocationMappers
from samples.WeatherApi.mappers.WeatherMappers import WeatherMappers
from samples.WeatherApi.models.Geolocation import Geolocation
from samples.WeatherApi.models.Weather import Weather
from samples.WeatherApi.services.BadWeatherServiceExample import BadWeatherServiceExample
from samples.WeatherApi.services.WeatherService import WeatherService
from samples.WeatherApi.tests.TestWeatherServiceConfigurationFactory import TestWeatherServiceConfigurationFactory


class WeatherServiceTests(unittest.TestCase):

    def setUp(self):
        weatherConfiguration: str = ('{'
                                     '  "BaseUrl": "http://api.openweathermap.org/",'
                                     '  "GeoLocationEndpoint": "geo/1.0/direct",'
                                     '  "DataEndpoint": "data/2.5/weather",'
                                     '  "Units": "metric"'
                                     '}')
        self.weatherApiConfiguration: WeatherServerConfiguration = TestWeatherServiceConfigurationFactory().get(weatherConfiguration)

        self.logger = Logger(__name__, 0, [getStdOutLogHandler()])

        self.weatherServices = [WeatherService(self.weatherApiConfiguration, GeolocationMappers(), WeatherMappers(), self.logger), BadWeatherServiceExample()]

    def test_CreateService(self):
        for service in self.weatherServices:
            self.assertIsNotNone(service, f"Could not create instance for {service.__class__.__name__}")

    def test_getCurrentWeather(self):
        for service in self.weatherServices:
            weather = service.getCurrentWeather('Sibiu', 'SB','RO')
            self.assertIsNotNone(weather, f"getCurrentWeather returned None for {service.__class__.__name__}")
            self.assertIsInstance(weather, Weather, f"getCurrentWeather did not return a Weather instance for {service.__class__.__name__}")
            self.assertIsNotNone(weather.temperature, f"getCurrentWeather did not return the correct temperature for {service.__class__.__name__}")
            self.assertIsNotNone(weather.minTemperature, f"getCurrentWeather did not return the correct minTemperature for {service.__class__.__name__}")
            self.assertIsNotNone(weather.maxTemperature, f"getCurrentWeather did not return the correct maxTemperature for {service.__class__.__name__}")
            self.assertIsNotNone(weather.feelsLike, f"getCurrentWeather did not return the correct feelsLike for {service.__class__.__name__}")
            self.assertIsNotNone(weather.visibility, f"getCurrentWeather did not return the correct visibility for {service.__class__.__name__}")

import unittest

from samples.WeatherApi.configurations.LoggerConfiguration import LoggerConfiguration
from samples.WeatherApi.configurations.WeatherServerConfiguration import WeatherServerConfiguration
from samples.WeatherApi.logger.Logger import Logger, getStdOutLogHandler
from samples.WeatherApi.configurations.Dynamic import Dynamic
from samples.WeatherApi.mappers.GeolocationMappers import GeolocationMappers
from samples.WeatherApi.mappers.WeatherMappers import WeatherMappers
from samples.WeatherApi.models.Geolocation import Geolocation
from samples.WeatherApi.models.Weather import Weather
from samples.WeatherApi.services.WeatherService import WeatherService


class WeatherServiceTests(unittest.TestCase):
    def setUp(self):
        self.weatherApiConfiguration: WeatherServerConfiguration = Dynamic.fromFile('WeatherServiceTestConfig.json')
        self.logConfiguration: LoggerConfiguration = Dynamic.fromFile('ConsoleLoggerTestConfig.json')
        self.logger = Logger(__name__, self.logConfiguration.Level, [getStdOutLogHandler()])

    def test_CreateService(self):
        service = WeatherService(self.weatherApiConfiguration, GeolocationMappers(), WeatherMappers(), self.logger)
        self.assertIsNotNone(service, "Could not create WeatherService instance")

    def test_getCoordinates(self):
        service = WeatherService(self.weatherApiConfiguration, GeolocationMappers(), WeatherMappers(), self.logger)
        location = service.getGeolocation('Sibiu', 'SB', 'RO')
        self.assertIsNotNone(location, "getCoordinates returned None")
        self.assertIsInstance(location, Geolocation, "getCoordinates did not return a Geolocation instance")
        self.assertEqual(location.name, 'Sibiu', "getCoordinates did not return the correct name")
        self.assertIsNotNone(location.longitude, "getCoordinates did not return the corsrect longitude")
        self.assertIsNotNone(location.latitude, "getCoordinates did not return the correct latitude")
        self.assertEqual(location.country, 'RO', "getCoordinates did not return the correct country")

    def test_getCurrentWeather(self):
        service = WeatherService(self.weatherApiConfiguration, GeolocationMappers(), WeatherMappers(), self.logger)
        weather = service.getCurrentWeather('Sibiu', 'SB','RO')
        self.assertIsNotNone(weather, "getCurrentWeather returned None")
        self.assertIsInstance(weather, Weather, "getCurrentWeather did not return a Weather instance")
        self.assertIsNotNone(weather.temperature, "getCurrentWeather did not return the correct temperature")
        self.assertIsNotNone(weather.minTemperature, "getCurrentWeather did not return the correct minTemperature")
        self.assertIsNotNone(weather.maxTemperature, "getCurrentWeather did not return the correct maxTemperature")
        self.assertIsNotNone(weather.feelsLike, "getCurrentWeather did not return the correct feelsLike")
        self.assertIsNotNone(weather.visibility, "getCurrentWeather did not return the correct visibility")

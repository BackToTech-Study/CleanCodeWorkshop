import unittest

from samples.WeatherApi.models.Weather import Weather
from samples.WeatherApi.services.BadWeatherServiceExample import BadWeatherServiceExample


class WeatherServiceTests(unittest.TestCase):

    def test_CreateService(self):
        service = BadWeatherServiceExample()
        self.assertIsNotNone(service, "Could not create WeatherService instance")

    def test_getCurrentWeather(self):
        service = BadWeatherServiceExample()
        weather = service.getCurrentWeather('Sibiu', 'SB','RO')
        self.assertIsNotNone(weather, "getCurrentWeather returned None")
        self.assertIsInstance(weather, Weather, "getCurrentWeather did not return a Weather instance")
        self.assertIsNotNone(weather.temperature, "getCurrentWeather did not return the correct temperature")
        self.assertIsNotNone(weather.minTemperature, "getCurrentWeather did not return the correct minTemperature")
        self.assertIsNotNone(weather.maxTemperature, "getCurrentWeather did not return the correct maxTemperature")
        self.assertIsNotNone(weather.feelsLike, "getCurrentWeather did not return the correct feelsLike")
        self.assertIsNotNone(weather.visibility, "getCurrentWeather did not return the correct visibility")

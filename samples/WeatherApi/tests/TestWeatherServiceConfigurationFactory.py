import os

from samples.WeatherApi.configurations.ConfigurationFactoryDecorator import ConfigurationFactoryDecorator
from samples.WeatherApi.configurations.JsonConfigurationFactory import JsonConfigurationFactory
from samples.WeatherApi.configurations.WeatherServerConfiguration import WeatherServerConfiguration


class TestWeatherServiceConfigurationFactory(ConfigurationFactoryDecorator):
    def __init__(self):
        super().__init__(JsonConfigurationFactory())

    def get(self, source: str) -> WeatherServerConfiguration:
        result: WeatherServerConfiguration = self.configurationFactory.get(source)
        result.ApiKey = os.getenv('API_KEY')
        return result

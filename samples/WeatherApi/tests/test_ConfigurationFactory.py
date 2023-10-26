import unittest
from datetime import datetime

from samples.WeatherApi.configurations.IConfigurationFactory import IConfigurationFactory
from samples.WeatherApi.configurations.JsonConfigurationFactory import JsonConfigurationFactory


class ConfigurationFactoryTests(unittest.TestCase):
    config: str = ""
    configurationFactory: IConfigurationFactory = JsonConfigurationFactory()

    def setUp(self):
        self.config = ('{'
                       '    "WeatherServer": { '
                       '        "BaseUrl": "http://api.openweathermap.org/"'
                       '    }'
                       '}')

    def test_CreateConfigurationFromFile(self):
        config = self.configurationFactory.get(self.config)
        self.assertIsNotNone(config, "Could not create ConfigurationFactory instance")

    def test_mappingFields(self):
        config = self.configurationFactory.get(self.config)
        self.assertIsNotNone(config.WeatherServer, "Config is missing the weatherApi section")
        self.assertIsNotNone(config.WeatherServer.BaseUrl, "Config is missing the weatherApi baseUrl")

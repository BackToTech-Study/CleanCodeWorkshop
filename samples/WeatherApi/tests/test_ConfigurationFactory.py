import os.path
import unittest
from datetime import datetime

from samples.WeatherApi.configurations.FileConfigurationFactory import FileConfigurationFactory


class ConfigurationFactoryTests(unittest.TestCase):
    configFile: str = ""
    configurationFactory: FileConfigurationFactory = FileConfigurationFactory()

    def setUp(self):
        now = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        self.configFile = f'ConfigurationFactoryConfig_{now}.json'
        with open(self.configFile, 'w') as f:
            f.write('{'
                    ' "WeatherServer": { '
                    '    "BaseUrl": "http://api.openweathermap.org/"'
                    ' }'
                    '}')

    def tearDown(self):
        if os.path.exists(self.configFile) and os.path.isfile(self.configFile):
            os.remove(self.configFile)

    def test_CreateConfigurationFromFile(self):
        config = self.configurationFactory.get(self.configFile)
        self.assertIsNotNone(config, "Could not create ConfigurationFactory instance")

    def test_mappingFields(self):
        config = self.configurationFactory.get(self.configFile)
        self.assertIsNotNone(config.WeatherServer, "Config is missing the weatherApi section")
        self.assertIsNotNone(config.WeatherServer.BaseUrl, "Config is missing the weatherApi baseUrl")

from .ConfigurationFactoryDecorator import ConfigurationFactoryDecorator
from .Dynamic import Dynamic
from .JsonConfigurationFactory import JsonConfigurationFactory


class FileConfigurationFactory(ConfigurationFactoryDecorator):
    def __init__(self):
        super().__init__(JsonConfigurationFactory())

    def get(self, fileName: str):
        with open(fileName) as inputStream:
            rawData = inputStream.read()
        if rawData is None:
            return Dynamic()
        return self.configurationFactory.get(rawData)

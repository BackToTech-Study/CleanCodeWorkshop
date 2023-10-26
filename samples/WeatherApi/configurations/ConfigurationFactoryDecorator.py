from abc import abstractmethod
from samples.WeatherApi.configurations.IConfigurationFactory import IConfigurationFactory


class ConfigurationFactoryDecorator(IConfigurationFactory):
    def __init__(self, configurationFactory: IConfigurationFactory):
        self.configurationFactory = configurationFactory

    @abstractmethod
    def get(self, configData):
        pass

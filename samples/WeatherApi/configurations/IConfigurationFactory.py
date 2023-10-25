from abc import ABC, abstractmethod

from samples.WeatherApi.configurations.Configuration import Configuration


class IConfigurationFactory(ABC):
    @abstractmethod
    def get(self, configData) -> Configuration:
        pass

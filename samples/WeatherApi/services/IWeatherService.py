from abc import ABC, abstractmethod

from samples.WeatherApi.models.Weather import Weather


class IWeatherService(ABC):
    @abstractmethod
    def getCurrentWeather(self, city: str, stateCode: str, countryCode: str) -> Weather or None:
        pass

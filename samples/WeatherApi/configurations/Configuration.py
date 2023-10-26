from samples.WeatherApi.configurations.Dynamic import Dynamic
from samples.WeatherApi.configurations.LoggerConfiguration import LoggerConfiguration
from samples.WeatherApi.configurations.WeatherServerConfiguration import WeatherServerConfiguration


class Configuration:
    @property
    def Logger(self) -> LoggerConfiguration:
        return self.Logger

    @property
    def WeatherServer(self) -> WeatherServerConfiguration:
        return self.WeatherServer

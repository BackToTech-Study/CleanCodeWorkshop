from samples.WeatherApi.configurations.Dynamic import Dynamic
from samples.WeatherApi.configurations.IConfigurationFactory import IConfigurationFactory


class JsonConfigurationFactory(IConfigurationFactory):
    def get(self, json: str):
        return Dynamic.fromJson(json)

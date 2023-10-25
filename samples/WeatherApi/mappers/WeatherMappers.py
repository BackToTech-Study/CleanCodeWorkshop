from samples.WeatherApi.models.Weather import Weather


class WeatherMappers:
    def mapJsonToWeather(self, json) -> Weather:
        result = Weather()
        result.temperature = json['main']['temp']
        result.minTemperature = json['main']['temp_min']
        result.maxTemperature = json['main']['temp_max']
        result.feelsLike = json['main']['feels_like']
        result.visibility = json['visibility']
        return result

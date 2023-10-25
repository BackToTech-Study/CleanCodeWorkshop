from samples.WeatherApi.models.Geolocation import Geolocation


class GeolocationMappers:
    def mapJsonToGeolocation(self, json) -> Geolocation:
        result = Geolocation()
        result.name = json['name']
        result.longitude = json['lon']
        result.latitude = json['lat']
        result.country = json['country']
        return result

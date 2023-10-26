from samples.WeatherApi.configurations.Dynamic import Dynamic


class WeatherServerConfiguration:

    @property
    def BaseUrl(self) -> str:
        return self.BaseUrl

    @property
    def GeoLocationEndpoint(self) -> str:
        return self.GeoLocationEndpoint

    @property
    def DataEndpoint(self) -> str:
        return self.DataEndpoint

    @property
    def Units(self) -> str:
        return self.Units

    @property
    def ApiKey(self) -> str:
        return self.ApiKey

    @ApiKey.setter
    def ApiKey(self, value) -> str:
        self.ApiKey = value

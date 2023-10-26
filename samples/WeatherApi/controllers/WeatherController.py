import jsonpickle
from flask import Blueprint, request

from samples.WeatherApi.helpers.HttpHelpers import getParameterValue
from samples.WeatherApi.logger.ILogger import ILogger
from samples.WeatherApi.services.IWeatherService import IWeatherService

weatherController = Blueprint('WeatherController', __name__)


@weatherController.route('', methods=['GET'])
def getCurrentWeather(weatherService: IWeatherService, logger: ILogger):
    city, error = getParameterValue(str, 'City', request)
    if city is None:
        logger.error(f"City parameter error: {error}")
        return "City is not specified", 400

    country, error = getParameterValue(str, 'CountryCode', request)
    if country is None:
        country = ''
        logger.error(f"Country parameter error: {error}")

    region, error = getParameterValue(str, 'RegionCode', request)
    if region is None:
        region = ''
        logger.error(f"Region parameter error: {error}")

    weather = weatherService.getCurrentWeather(country, region, city)
    return jsonpickle.encode(weather, unpicklable=False), 200

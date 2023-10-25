from flask import Flask
import flask_injector

from samples.WeatherApi.configurations.FileConfigurationFactory import FileConfigurationFactory
from samples.WeatherApi.configurations.WeatherServerConfiguration import WeatherServerConfiguration
from samples.WeatherApi.controllers.WeatherController import weatherController
from samples.WeatherApi.logger.Logger import getStdOutLogHandler, Logger
from samples.WeatherApi.mappers.GeolocationMappers import GeolocationMappers
from samples.WeatherApi.mappers.WeatherMappers import WeatherMappers
from samples.WeatherApi.services.IWeatherService import IWeatherService
from samples.WeatherApi.services.WeatherService import WeatherService


class WeatherServer:
    pass


def create_app(configFileName='Configuration.json'):
    app = Flask(__name__)

    app.register_blueprint(weatherController, url_prefix='/weather')

    configuration = FileConfigurationFactory().get(configFileName)

    def configureDependencies(binder):
        binder.bind(GeolocationMappers, to=GeolocationMappers(), scope=flask_injector.request)
        binder.bind(WeatherMappers, to=WeatherMappers(), scope=flask_injector.request)
        binder.bind(WeatherServerConfiguration, to=configuration.WeatherServer, scope=flask_injector.request)
        binder.bind(Logger, to=Logger(__name__, configuration.Logger.Level, [getStdOutLogHandler()]), scope=flask_injector.request)
        binder.bind(IWeatherService, to=WeatherService, scope=flask_injector.request)

    flask_injector.FlaskInjector(app=app, modules=[configureDependencies])

    return app

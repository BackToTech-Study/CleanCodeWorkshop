# CleanCodeWorkshop
Share ideas and recommendations for clean implementations

## Clean Code
Your code should be as easy to read as a newspaper.
Code is like a joke. If you have to explain it, it's bad.
Make your life easier. Write clean code.

### Resources
* Clean Code - Robert C. Martin
* Don't make me think - Steve Krug
* Clean Architecture - Robert C. Martin

## SOLID
* Single Responsibility Principle - A module should have one, and only one, reason to change.
* Open/Closed Principle - Software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification.
* Liskov Substitution Principle - Objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program.
* Interface Segregation Principle - Many client-specific interfaces are better than one general-purpose interface.
* Dependency Inversion Principle - One should depend upon abstractions, not concretions.

## Design patterns
Patterns are not solutions. 
They are, battle tested, reusable, software design concepts that can be applied to solve problems.
Design patterns help use to write clean code.

### Resources
* Design Patterns: Elements of Reusable Object-Oriented Software -  Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, Grady Booch
* Head First Design Patterns -  Eric Freeman, Bert Bates, Kathy Sierra, Elisabeth Robson

## Examples

### Your code should be as easy to read as a newspaper.

Can you understand this function? Why?
```python
    def getCurrentWeather(self, city: str, stateCode: str, countryCode: str) -> Weather or None:
        location: Geolocation = self.__getGeolocation(city, stateCode, countryCode)
        if location is None:
            return None

        parameters = {'lat': location.latitude, 'lon': location.longitude, 'units': self.__units,  'appid': self.__apiKey}
        result = requests.get(self.__dataUrl, params=parameters)

        if result is None or isNotPositiveResponse(result.status_code):
            return None

        try:
            data = result.json()
            return self.__weatherMapper.fromJson(data)
        except KeyError as error:
            self.__logger.error(f"Missing key in weather data for {city},{stateCode},{countryCode}: {error}")
            return None
        except Exception as error:
            self.__logger.error(f"Unexpected weather data for {city},{stateCode},{countryCode}: {error}")
            return None
```

### Your solution design should be easy to read

What are the folders you would expect when using MVC?
![mvc.png](images%2Fmvc.png)
* Avoid hybrid structures (half object and half data).
* Single Responsibility Principle - A module should have one, and only one, reason to change.

**Design patterns improves our ability to communicate with other developers.**

### Favor polymorphism to if/else cascade or switch/case
**Don't use flag arguments. Split method into several independent methods that can be called from the client without the flag.**
```python
class Logger(ILogger):
    def __init__(self, loggerName: str, level: int, handlerCollection: []):
        ...
        for handler in handlerCollection:
            self.addHandler(handler)
        ...
```

```python
def getStdOutLogHandler():
    handler = logging.StreamHandler()
    handler.setFormatter(getFormatter())
    return handler
```

```python
    class StreamHandler(Handler):
```

```python
def getRollingFileLogHandler(fileName, maxBytes, backupCount):
    handler = RotatingFileHandler(fileName, maxBytes=maxBytes, backupCount=backupCount)
    handler.setFormatter(getFormatter())
    return handler
```

```python
    class RotatingFileHandler(BaseRotatingHandler):
    ...
    class BaseRotatingHandler(logging.FileHandler):
    ...
    class FileHandler(StreamHandler):
```

```python
def callHandlers(self, record):
    """
    Pass a record to all relevant handlers.

    Loop through all handlers for this logger and its parents in the
    logger hierarchy. If no handler was found, output a one-off error
    message to sys.stderr. Stop searching up the hierarchy whenever a
    logger with the "propagate" attribute set to zero is found - that
    will be the last logger whose handlers are called.
    """
    c = self
    found = 0
    while c:
        for hdlr in c.handlers:
            found = found + 1
            if record.levelno >= hdlr.level:
                hdlr.handle(record)
        if not c.propagate:
            c = None    #break out
        else:
            c = c.parent
```

### Design patterns make heavy use of polymorphisms
**Decorator Pattern**
![decorator.png](images%2Fdecorator.png)

```python
class IConfigurationFactory(ABC):
    @abstractmethod
    def get(self, configData):
        pass
```

```python
class JsonConfigurationFactory(IConfigurationFactory):
    def get(self, json: str):
        return Dynamic.fromJson(json)
```

```python
class FileConfigurationFactory(ConfigurationFactoryDecorator):
    def __init__(self):
        super().__init__(JsonConfigurationFactory())

    def get(self, fileName: str):
        with open(fileName) as inputStream:
            rawData = inputStream.read()
        if rawData is None:
            return Dynamic()
        return self.configurationFactory.get(rawData)
```

```python
class ConfigurationFactoryDecorator(IConfigurationFactory):
    def __init__(self, configurationFactory: IConfigurationFactory):
        self.configurationFactory = configurationFactory

    @abstractmethod
    def get(self, configData):
        pass
```

```python
class TestWeatherServiceConfigurationFactory(ConfigurationFactoryDecorator):
    def __init__(self):
        super().__init__(JsonConfigurationFactory())

    def get(self, source: str) -> WeatherServerConfiguration:
        result: WeatherServerConfiguration = self.configurationFactory.get(source)
        result.ApiKey = os.getenv('API_KEY')
        return result

```

**Liskov Substitution Principle - Objects in a program should be replaceable with instances of their subtypes without altering the correctness of that program.**

**Dependency Inversion Principle - Depend on abstractions, not concrete instances.**


### Make your code testable by using dependency injection
```python
    def getCurrentWeather(self, city: str, stateCode: str, countryCode: str) -> Weather or None:
        ...
        
        parameters = {'lat': location.latitude, 'lon': location.longitude, 'units': self.__units,  'appid': self.__apiKey}
        ...

        try:
            ...
            return self.__weatherMapper.fromJson(data)
        except KeyError as error:
            self.__logger.error(f"Missing key in weather data for {city},{stateCode},{countryCode}: {error}")
            return None
        except Exception as error:
            self.__logger.error(f"Unexpected weather data for {city},{stateCode},{countryCode}: {error}")
            return None
```
```python
    @inject
    def __init__(self,
                 weatherConfiguration: WeatherServerConfiguration,
                 geolocationMapper: GeolocationMappers,
                 weatherMapper: WeatherMappers,
                 logger: ILogger):
        self.__apiKey = weatherConfiguration.ApiKey
        self.__geoLocationUrl = weatherConfiguration.BaseUrl+weatherConfiguration.GeoLocationEndpoint
        self.__dataUrl = weatherConfiguration.BaseUrl+weatherConfiguration.DataEndpoint
        self.__units = weatherConfiguration.Units
        self.__geolocationMapper = geolocationMapper
        self.__weatherMapper = weatherMapper
        self.__logger = logger
```

```python
    def configureDependencies(binder):
        binder.bind(GeolocationMappers, to=GeolocationMappers(), scope=flask_injector.request)
        binder.bind(WeatherMappers, to=WeatherMappers(), scope=flask_injector.request)
        binder.bind(WeatherServerConfiguration, to=configuration.WeatherServer, scope=flask_injector.request)
        binder.bind(ILogger, to=Logger(__name__, configuration.Logger.Level, [getStdOutLogHandler()]), scope=flask_injector.request)
        binder.bind(IWeatherService, to=WeatherService, scope=flask_injector.request)
```

```python
    def setUp(self):
        weatherConfiguration: str = ('{'
                                     '  "BaseUrl": "http://api.openweathermap.org/",'
                                     '  "GeoLocationEndpoint": "geo/1.0/direct",'
                                     '  "DataEndpoint": "data/2.5/weather",'
                                     '  "Units": "metric"'
                                     '}')
        self.weatherApiConfiguration: WeatherServerConfiguration = TestWeatherServiceConfigurationFactory().get(weatherConfiguration)
        
        self.logger = Logger(__name__, 0, [getStdOutLogHandler()])
        
        self.weatherServices = [WeatherService(self.weatherApiConfiguration, GeolocationMappers(), WeatherMappers(), self.logger), BadWeatherServiceExample()]


    def test_CreateService(self):
        for service in self.weatherServices:
            self.assertIsNotNone(service, f"Could not create instance for {service.__class__.__name__}")
```

```python
class Logger:
    def __init__(self, loggerName: str, level: int, handlerCollection: []):
        ...
        for handler in handlerCollection:
            self.addHandler(handler)
        ...
```

### Dependency inversion in the Command Pattern

How would you implement support for a list of commands? (Go to design editor)

**Dependency Inversion Principle - One should depend upon abstractions, not concretions.**

![command pattern.png](images%2Fcommand%20pattern.png)

```python
class UserInterface:
    def __init__(self, addCommand: ICommand, subtractCommand: ICommand, multiplyCommand: ICommand, divideCommand: ICommand):
        self.__addCommand = addCommand
        self.__subtractCommand = subtractCommand
        self.__multiplyCommand = multiplyCommand
        self.__divideCommand = divideCommand
        self.__executedCommands = []
        self.__undoneCommands = []
```

```python
class ICommand(ABC):
    @abstractmethod
    def execute(self, value: float) -> float:
        pass

    @abstractmethod
    def undo(self, value: float) -> float:
        pass
```

```python
class AddCommand(ICommand):
    def __init__(self, calculator: Calculator):
        self.__calculator = calculator

    def execute(self, value: float) -> float:
        self.__calculator.add(value)
        return self.__calculator.currentValue

    def undo(self, value: float) -> float:
        self.__calculator.subtract(value)
        return self.__calculator.currentValue
```

**Favor Composition over inheritance.**

**Stable software architectures favor dependency on stable abstract interfaces. Stable components should not depend on volatile components.**

### Limit dependencies. Avoid side effects. See the concept of pure functions.


## Code smells
* **Rigidity**. The software is difficult to change. A small change causes a cascade of subsequent changes.
* **Fragility**. The software breaks in many places due to a single change.
* **Immobility**. You cannot reuse parts of the code in other projects because of involved risks and high effort.
* **Needless Repetition**.
* **The code is hard to understand**.
* _**Needless Complexity**._

### Keep configuration data away from the source code.
```python
    def getCurrentWeather(self, city: str, code: str, country: str) -> Weather or None:
        key = "some key"
        p = {'q': f'{city},{code},{country}', 'limit': 1, 'appid': key}
        r = requests.get("http://api.openweathermap.org/geo/1.0/direct", params=p)

        try:
            loc = self.__geolocationMapper.mapJsonToGeolocation(r.json()[0])
            p = {'lat': loc.latitude, 'lon': loc.longitude, 'appid': key}
            r = requests.get("http://api.openweathermap.org/data/2.5/weather", params=p)
            return self.__weatherMapper.mapJsonToWeather(r.json())
        except Exception as error:
            self.__log.error(f"{error}")
            return None
```

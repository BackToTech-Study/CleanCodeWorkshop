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

The invoker is not aware of how the command is executed, it only knows what command to invoke. 
So the **command pattern helps us implement separation of concerns**, 
because the invoker and receiver can change independently of each other.

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

C# examples here: 
* https://github.com/BackToTech-Study/CommandPattern

Presentation here:
* https://youtu.be/lv5u7D4RoOg

### Limit dependencies.

**A pure function has no side effects. For the same input value it will always generate the same result.**
Pure functions are easier to test and reuse.

```python
def isNotPositiveResponse(statusCode):
    return statusCode < 200 or statusCode > 300
```

```python
def turnOn(self) -> None:
    self.__currentState = On(self, self.__log)

def turnOff(self) -> None:
    self.__currentState = Off(self, self.__log)

def update(self) -> None:
    self.__log.info("Motion detected.")
    self.__currentState.processMotionDetected()
```        


### Decoupling with the Observer Pattern

The observer pattern helps implement pushing updates from one object (subject) to a runtime dynamic list of interested objects (observers).
![observer pattern.png](images%2Fobserver%20pattern.png)
The **subject is not dependent on the implementation of the observer** because 
the subject only knows that the observer implements the observer interface.

```python
class MockMotionSensor(IMotionSensor):
    ...
    
    def subscribe(self, observer: IObserver) -> None:
        if observer is not None:
            self.__observerCollection.append(observer)

    def unsubscribe(self, observer: IObserver) -> None:
        if observer is not None:
            self.__observerCollection.remove(observer)

    def __notifyObservers(self) -> None:
        ...
        for observer in self.__observerCollection:
            observer.update()
        ...
```

```python
class IObserver(ABC):
    @abstractmethod
    def update(self) -> None:
        pass
```

```python
class LightSystem(IObserver):
    ...
    def update(self) -> None:
        self.__log.info("Motion detected.")
        self.__currentState.processMotionDetected()
```

C# examples here: 
* https://github.com/BackToTech-Study/ObserverPattern
* https://learn.microsoft.com/en-us/dotnet/standard/events/observer-design-pattern

Presentation here:
* https://youtu.be/9e6ZQTftg08

### State Pattern

Design patterns are usually bundled together.

![state pattern theory.png](images%2Fstate%20pattern%20theory.png)

Example:
![state pattern.png](images%2Fstate%20pattern.png)

All states implement the same interface, 
so adding new states to a state machine can be done without touching the code of the other states. 
For this reason, using the **sate design patterns helps implement the open-close principle.**

```python
class LightSystem(IObserver):
    def __init__(self, log: ILogger, timeout: int or None = None):
        ...
        self.turnOff()
        ...
    
    def turnOn(self) -> None:
        self.__currentState = On(self, self.__log)

    def turnOff(self) -> None:
        self.__currentState = Off(self, self.__log)

    def update(self) -> None:
        self.__log.info("Motion detected.")
        self.__currentState.processMotionDetected()
```

```python
class ILightState(ABC):
    @abstractmethod
    def processMotionDetected(self) -> None:
        pass
```

```python
class Off(ILightState):
    def __init__(self, light, log: ILogger):
        log.info("Turn off lights.")
        self.__light = light

    def processMotionDetected(self) -> None:
        self.__light.turnOn()
```

```python
class On(ILightState):
    def __init__(self, light, log: ILogger):
        ...
        self.__log.info("Turn on lights.")
        self.__light = light
        
        self.__timeoutTask = self.__getTimeoutTask()
        self.__timeoutTask.start()
        
    def __getTimeoutTask(self) -> Timer:
        return Timer(self.__light.timeout, self.__turnOffAfterTimeout, [])

    def __turnOffAfterTimeout(self):
        self.__log.info("Inactivity timeout reached.")
        self.__light.turnOff()        

    def processMotionDetected(self) -> None:
        self.__timeoutTask.cancel()
        self.__timeoutTask = self.__getTimeoutTask()
        self.__timeoutTask.start()
```

## Code smells
Using design patterns bring best code practices to your code.
But they also add needless complexity.

What to look for?

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

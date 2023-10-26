from samples.ObserverPattern.LightSystemSimulation.Lights.LightSystem import LightSystem
from samples.ObserverPattern.LightSystemSimulation.Logger.Logger import Logger
from samples.ObserverPattern.LightSystemSimulation.MotionSensor.IMotionSensor import IMotionSensor
from samples.ObserverPattern.LightSystemSimulation.MotionSensor.MockMotionSensor import MockMotionSensor

simulationDetectionCycle = 5
livingRoomSensor: IMotionSensor = MockMotionSensor(simulationDetectionCycle)

logger = Logger()
inactivityTimeout = 2
livingRoomLighting = LightSystem(logger, inactivityTimeout)

livingRoomSensor.subscribe(livingRoomLighting)

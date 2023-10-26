from samples.CommandPattern.Commands.ICommand import ICommand


class ExecutedCommand:
    def __init__(self, command: ICommand, value: float):
        self.__command = command
        self.__value = value

    @property
    def command(self):
        return self.__command

    @property
    def value(self):
        return self.__value

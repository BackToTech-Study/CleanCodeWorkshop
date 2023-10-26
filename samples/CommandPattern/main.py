from samples.CommandPattern.Client.Client import Client
from samples.CommandPattern.Invoker.UserInterface import UserInterface

client = Client()
user = UserInterface(client.addCommand, client.subtractCommand, client.multiplyCommand, client.divideCommand)
user.listenForCommands()

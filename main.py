from storage.database import Database
from engine.command_executor import CommandExecutor
from connection.client_session import ClientSession


db = Database(capacity=1000)

executor = CommandExecutor(db)


def create_session():

    return ClientSession(executor)
from storage.database import Database
from engine.command_executor import CommandExecutor
from connection.client_session import ClientSession


# One shared database
db = Database(capacity=1000)

# One shared executor
executor = CommandExecutor(db)


def create_session():

    return ClientSession(executor)


def process(session, data):

    return session.process(data)
from storage.database import Database
from engine.command_executor import CommandExecutor
from connection.client_session import ClientSession
from persistence.aof import AOF

from engine.command import Command


db = Database(capacity=1000)

aof = AOF("appendonly.aof")

executor = CommandExecutor(
    db,
    aof
)


def recover():

    for parts in aof.load():
        if not parts:
            continue

        
        command_name=parts[0]
        arguments=parts[1:]

        command = Command(
            command_name,
            arguments
        )

        executor.execute(
            command,
            from_recovery=True
        )


recover()


def create_session():

    return ClientSession(executor)


def process(session, data):

    return session.process(data)
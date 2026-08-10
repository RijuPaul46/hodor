from parser.parser import Parser
from engine.command_executor import CommandExecutor
from storage.database import Database


db = Database(capacity=1000)

parser = Parser()

executor = CommandExecutor(db)


def process_command(text):

    command = parser.parse(text)
    if command is None :
        return "EMPTY COMMAND"

    result = executor.execute(command)

    return result
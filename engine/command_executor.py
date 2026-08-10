from commands.string_commands import StringCommands
from commands.hash_commands import HashCommands


class CommandExecutor:

    def __init__(self, db):

        self.string = StringCommands(db)
        self.hash = HashCommands(db)

        self.handlers = {
            "SET": self.string.set,
            "GET": self.string.get,
            "DEL": self.string.delete,

            "HSET": self.hash.hset,
            "HGET": self.hash.hget,
        }

    def execute(self, command):

        cmd = command.command

        handler = self.handlers.get(cmd)

        if handler is None:
            return "UNKNOWN COMMAND"

        return handler(*command.arguments)
from commands.string_commands import StringCommands
from commands.hash_commands import HashCommands


class CommandExecutor:

    def __init__(self, db, aof=None):

        self.db = db

        self.aof = aof

        self.string = StringCommands(db)
        self.hash = HashCommands(db)

        self.handlers = {
            "SET": self.string.set,
            "GET": self.string.get,
            "DEL": self.string.delete,

            "HSET": self.hash.hset,
            "HGET": self.hash.hget,
        }

    def execute(self, command, from_recovery=False):

        cmd = command.command

        handler = self.handlers.get(cmd)

        if handler is None:
            return "UNKNOWN COMMAND"

        result = handler(
            *command.arguments
        )

        # Don't write replayed commands
        # back into the AOF.
        if (
            self.aof is not None
            and not from_recovery
            and cmd in {"SET", "DEL", "HSET"}
        ):
            self.aof.append(command)

        return result
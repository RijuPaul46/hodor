from engine.command import Command
from persistence.aof import AOF


aof = AOF("test.aof")

aof.append(
    Command(
        "SET",
        ["name", "Riju"]
    )
)

aof.append(
    Command(
        "SET",
        ["age", "20"]
    )
)

aof.append(
    Command(
        "DEL",
        ["age"]
    )
)

print("\nCommands stored in AOF:\n")

for command, arguments in aof.load():

    print(
        "Command:",
        command,
        "Arguments:",
        arguments
    )

aof.close()
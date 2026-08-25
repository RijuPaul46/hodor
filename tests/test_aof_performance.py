import time

from engine.command import Command
from persistence.aof import AOF


COMMAND_COUNT = 1000


aof = AOF(
    "benchmark.aof",
    fsync=True
)


start = time.perf_counter()


for i in range(COMMAND_COUNT):

    command = Command(
        "SET",
        [f"key{i}", f"value{i}"]
    )

    aof.append(command)


elapsed = time.perf_counter() - start

aof.close()


print(
    f"Commands: {COMMAND_COUNT}"
)

print(
    f"Time: {elapsed:.4f} seconds"
)

print(
    f"Throughput: "
    f"{COMMAND_COUNT / elapsed:.2f} commands/sec"
)
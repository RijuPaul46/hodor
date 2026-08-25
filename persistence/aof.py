import os

from protocol.hsp_encoder import HSPEncoder
from protocol.hsp_parser import HSPParser


class AOF:

    def __init__(
        self,
        filename="appendonly.aof",
        fsync=True
    ):

        self.filename = filename

        self.fsync_enabled = fsync

        self.file = open(
            self.filename,
            "ab"
        )

    def append(self, command):

        parts = [
            command.command
        ] + command.arguments

        data = HSPEncoder.array(parts)

        self.file.write(data)

        self.file.flush()

        if self.fsync_enabled:

            os.fsync(
                self.file.fileno()
            )

    def load(self):

        self.file.flush()

        parser = HSPParser()

        with open(
            self.filename,
            "rb"
        ) as file:

            while True:

                data = file.read(4096)

                if not data:
                    break

                messages = parser.feed(data)

                for message in messages:

                    yield message

    def close(self):

        self.file.close()
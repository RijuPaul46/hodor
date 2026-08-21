from protocol.hsp_parser import HSPParser
from protocol.hsp_encoder import HSPEncoder

from engine.command import Command


class ClientSession:

    def __init__(self, executor):

        self.parser = HSPParser()

        self.executor = executor


    def process(self, data):

        parts = self.parser.feed(data)

        # Message is incomplete
        if parts is None:
            return None

        # HSP request should be an array
        if not isinstance(parts, list):
            return HSPEncoder.error(
                "request must be an array"
            )

        if len(parts) == 0:
            return HSPEncoder.error(
                "empty command"
            )

        command_name = parts[0]

        arguments = parts[1:]

        command = Command(
            command_name.upper(),
            arguments
        )

        result = self.executor.execute(command)

        return HSPEncoder.encode(result)
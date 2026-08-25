from protocol.hsp_parser import HSPParser
from protocol.hsp_encoder import HSPEncoder

from engine.command import Command


class ClientSession:

    def __init__(self, executor):

        # One parser for this client connection
        self.parser = HSPParser()

        # Shared command executor
        self.executor = executor

    def process(self, data):

        # Feed newly received TCP bytes to this
        # client's parser.
        messages = self.parser.feed(data)

        # No complete HSP message yet
        if not messages:
            return None

        responses = []

        # Process every complete HSP message
        # found in this recv() call.
        for parts in messages:

            # --------------------------------------
            # Request must be an HSP array
            # --------------------------------------

            if not isinstance(parts, list):

                responses.append(
                    HSPEncoder.error(
                        "request must be an array"
                    )
                )

                continue

            # --------------------------------------
            # Empty array
            # --------------------------------------

            if len(parts) == 0:

                responses.append(
                    HSPEncoder.error(
                        "empty command"
                    )
                )

                continue

            # --------------------------------------
            # First element = command
            # --------------------------------------

            command_name = parts[0]

            # --------------------------------------
            # Remaining elements = arguments
            # --------------------------------------

            arguments = parts[1:]

            # --------------------------------------
            # Create Command object
            # --------------------------------------

            command = Command(
                command_name.upper(),
                arguments
            )

            # --------------------------------------
            # Execute command
            # --------------------------------------

            result = self.executor.execute(
                command
            )

            # --------------------------------------
            # Convert result to HSP bytes
            # --------------------------------------

            response = HSPEncoder.encode(
                result
            )

            responses.append(response)

        # Send all responses as one byte stream
        return b"".join(responses)
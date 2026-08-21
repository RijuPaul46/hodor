class IncompleteHSPMessage(Exception):
    """
    Raised when we don't have enough bytes yet
    to parse a complete HSP message.
    """
    pass


class HSPParser:

    def __init__(self):

        # TCP may give us only part of a message.
        # So we keep all received bytes here.
        self.buffer = b""

    # ==================================================
    # PUBLIC METHOD
    # ==================================================

    def feed(self, data):

        """
        Give newly received TCP bytes to the parser.

        If a complete HSP message exists:
            return the parsed Python value.

        If the message is incomplete:
            return None.
        """

        # Add newly received bytes to our buffer
        self.buffer += data

        try:

            # Try to parse one complete HSP value
            value, position = self._parse_value(
                self.buffer,
                0
            )

        except IncompleteHSPMessage:

            # We don't have enough data yet.
            # Keep everything in the buffer.
            return None

        # Remove the bytes that we successfully consumed.
        self.buffer = self.buffer[position:]

        return value

    # ==================================================
    # GENERAL VALUE PARSER
    # ==================================================

    def _parse_value(self, data, position):

        """
        Look at the first byte and decide
        which HSP type we are dealing with.
        """

        # Make sure there is at least one byte
        if position >= len(data):

            raise IncompleteHSPMessage()

        prefix = data[position:position + 1]

        # ----------------------------------------------
        # Simple String
        # ----------------------------------------------

        if prefix == b"+":

            return self._parse_simple_string(
                data,
                position
            )

        # ----------------------------------------------
        # Error
        # ----------------------------------------------

        elif prefix == b"-":

            return self._parse_error(
                data,
                position
            )

        # ----------------------------------------------
        # Integer
        # ----------------------------------------------

        elif prefix == b":":

            return self._parse_integer(
                data,
                position
            )

        # ----------------------------------------------
        # Bulk String
        # ----------------------------------------------

        elif prefix == b"$":

            return self._parse_bulk_string(
                data,
                position
            )

        # ----------------------------------------------
        # Array
        # ----------------------------------------------

        elif prefix == b"*":

            return self._parse_array(
                data,
                position
            )

        else:

            raise ValueError(
                f"Unknown HSP prefix: {prefix}"
            )

    # ==================================================
    # FIND CRLF
    # ==================================================

    def _find_crlf(self, data, start):

        """
        Search for \\r\\n starting from 'start'.

        If we haven't received the complete line yet,
        tell the caller that we need more TCP data.
        """

        end = data.find(
            b"\r\n",
            start
        )

        if end == -1:

            raise IncompleteHSPMessage()

        return end

    # ==================================================
    # SIMPLE STRING
    # ==================================================

    def _parse_simple_string(
        self,
        data,
        position
    ):

        """
        Example:

        +OK\\r\\n

        Result:

        "OK"
        """

        end = self._find_crlf(
            data,
            position + 1
        )

        value = data[
            position + 1 : end
        ].decode()

        # Move past \\r\\n
        next_position = end + 2

        return value, next_position

    # ==================================================
    # ERROR
    # ==================================================

    def _parse_error(
        self,
        data,
        position
    ):

        """
        Example:

        -ERR wrong type\\r\\n
        """

        end = self._find_crlf(
            data,
            position + 1
        )

        message = data[
            position + 1 : end
        ].decode()

        next_position = end + 2

        # For now represent HSP errors as Python Exception
        return Exception(message), next_position

    # ==================================================
    # INTEGER
    # ==================================================

    def _parse_integer(
        self,
        data,
        position
    ):

        """
        Example:

        :20\\r\\n

        Result:

        20
        """

        end = self._find_crlf(
            data,
            position + 1
        )

        number = int(
            data[
                position + 1 : end
            ]
        )

        next_position = end + 2

        return number, next_position

    # ==================================================
    # BULK STRING
    # ==================================================

    def _parse_bulk_string(
        self,
        data,
        position
    ):

        """
        Example:

        $4\\r\\nRiju\\r\\n

        Structure:

        $4\\r\\n
          ↑
          header

        Riju
          ↑
          exactly 4 payload bytes

        \\r\\n
          ↑
          payload terminator
        """

        # ----------------------------------------------
        # Find end of "$4"
        # ----------------------------------------------

        header_end = self._find_crlf(
            data,
            position + 1
        )

        # Example:
        #
        # data[position + 1 : header_end]
        #
        # gives:
        #
        # b"4"

        length = int(
            data[
                position + 1 : header_end
            ]
        )

        # ----------------------------------------------
        # NULL bulk string
        # ----------------------------------------------

        if length == -1:

            return None, header_end + 2

        # ----------------------------------------------
        # Payload starts after "$4\\r\\n"
        # ----------------------------------------------

        payload_start = header_end + 2

        # ----------------------------------------------
        # Payload ends after exactly 'length' bytes
        # ----------------------------------------------

        payload_end = (
            payload_start + length
        )

        # ----------------------------------------------
        # Check whether complete payload + CRLF exists
        # ----------------------------------------------

        if payload_end + 2 > len(data):

            raise IncompleteHSPMessage()

        # ----------------------------------------------
        # Verify payload's terminating CRLF
        # ----------------------------------------------

        if data[
            payload_end : payload_end + 2
        ] != b"\r\n":

            raise ValueError(
                "Invalid bulk string terminator"
            )

        # ----------------------------------------------
        # Extract exactly the payload bytes
        # ----------------------------------------------

        payload = data[
            payload_start : payload_end
        ]

        # Convert bytes → Python string
        payload = payload.decode()

        # Move after payload + CRLF
        next_position = payload_end + 2

        return payload, next_position

    # ==================================================
    # ARRAY
    # ==================================================

    def _parse_array(
        self,
        data,
        position
    ):

        """
        Example:

        *3\\r\\n
        $3\\r\\nSET\\r\\n
        $4\\r\\nname\\r\\n
        $4\\r\\nRiju\\r\\n

        Result:

        [
            "SET",
            "name",
            "Riju"
        ]
        """

        # ----------------------------------------------
        # Find end of "*3"
        # ----------------------------------------------

        header_end = self._find_crlf(
            data,
            position + 1
        )

        # Get number of array elements
        count = int(
            data[
                position + 1 : header_end
            ]
        )

        # First element starts after "*3\\r\\n"
        current_position = header_end + 2

        result = []

        # ----------------------------------------------
        # Parse every array element
        # ----------------------------------------------

        for _ in range(count):

            value, current_position = (
                self._parse_value(
                    data,
                    current_position
                )
            )

            result.append(value)

        return result, current_position

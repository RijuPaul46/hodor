class HSPParser:

    def parse(self, data):

        # We expect bytes from the socket
        if not isinstance(data, bytes):
            raise TypeError("HSP parser expects bytes")

        # Start reading from position 0
        value, position = self._parse_value(data, 0)

        # Make sure there is no unexpected data
        if position != len(data):
            raise ValueError("Extra data after HSP message")

        return value

    # ------------------------------------------------
    # Parse one HSP value
    # ------------------------------------------------

    def _parse_value(self, data, position):

        prefix = data[position:position + 1]

        # Simple String
        if prefix == b"+":
            return self._parse_simple_string(
                data,
                position
            )

        # Error
        elif prefix == b"-":
            return self._parse_error(
                data,
                position
            )

        # Integer
        elif prefix == b":":
            return self._parse_integer(
                data,
                position
            )

        # Bulk String
        elif prefix == b"$":
            return self._parse_bulk_string(
                data,
                position
            )

        # Array
        elif prefix == b"*":
            return self._parse_array(
                data,
                position
            )

        else:
            raise ValueError(
                f"Unknown HSP prefix: {prefix}"
            )

    # ------------------------------------------------
    # Find CRLF
    # ------------------------------------------------

    def _find_crlf(self, data, start):

        end = data.find(b"\r\n", start)

        if end == -1:
            raise ValueError("Incomplete HSP message")

        return end

    # ------------------------------------------------
    # Simple String
    # ------------------------------------------------

    def _parse_simple_string(self, data, position):

        end = self._find_crlf(
            data,
            position + 1
        )

        value = data[
            position + 1 : end
        ].decode()

        next_position = end + 2

        return value, next_position

    # ------------------------------------------------
    # Error
    # ------------------------------------------------

    def _parse_error(self, data, position):

        end = self._find_crlf(
            data,
            position + 1
        )

        message = data[
            position + 1 : end
        ].decode()

        next_position = end + 2

        return Exception(message), next_position

    # ------------------------------------------------
    # Integer
    # ------------------------------------------------

    def _parse_integer(self, data, position):

        end = self._find_crlf(
            data,
            position + 1
        )

        number = int(
            data[position + 1 : end]
        )

        next_position = end + 2

        return number, next_position

    # ------------------------------------------------
    # Bulk String
    # ------------------------------------------------

    def _parse_bulk_string(self, data, position):

        # Find the end of "$4"
        header_end = self._find_crlf(
            data,
            position + 1
        )

        length = int(
            data[position + 1 : header_end]
        )

        # NULL bulk string
        if length == -1:

            return None, header_end + 2

        # Start of actual payload
        payload_start = header_end + 2

        # End of payload
        payload_end = payload_start + length

        # Make sure the complete payload exists
        if payload_end + 2 > len(data):

            raise ValueError(
                "Incomplete bulk string"
            )

        # Verify payload terminator
        if data[payload_end:payload_end + 2] != b"\r\n":

            raise ValueError(
                "Invalid bulk string terminator"
            )

        payload = data[
            payload_start:payload_end
        ].decode()

        next_position = payload_end + 2

        return payload, next_position

    # ------------------------------------------------
    # Array
    # ------------------------------------------------

    def _parse_array(self, data, position):

        # Find the end of "*3"
        header_end = self._find_crlf(
            data,
            position + 1
        )

        count = int(
            data[position + 1 : header_end]
        )

        current_position = header_end + 2

        result = []

        for _ in range(count):

            value, current_position = self._parse_value(
                data,
                current_position
            )

            result.append(value)

        return result, current_position
class HSPEncoder:

    @staticmethod
    def simple_string(value):
        return f"+{value}\r\n".encode()

    @staticmethod
    def error(message):
        return f"-{message}\r\n".encode()

    @staticmethod
    def integer(value):
        return f":{value}\r\n".encode()

    @staticmethod
    def bulk_string(value):

        if value is None:
            return b"$-1\r\n"

        data = str(value).encode()

        return (
            f"${len(data)}\r\n".encode()
            + data
            + b"\r\n"
        )

    @staticmethod
    def array(values):

        result = f"*{len(values)}\r\n".encode()

        for value in values:
            result += HSPEncoder.encode(value)

        return result

    @staticmethod
    def encode(value):

        if value is None:
            return b"$-1\r\n"

        if isinstance(value, bool):
            return HSPEncoder.integer(int(value))

        if isinstance(value, int):
            return HSPEncoder.integer(value)

        if isinstance(value, str):
            return HSPEncoder.bulk_string(value)

        if isinstance(value, list):
            return HSPEncoder.array(value)

        raise TypeError(
            f"Unsupported HSP type: {type(value)}"
        )
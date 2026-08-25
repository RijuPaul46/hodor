import socket
import shlex

from protocol.hsp_encoder import HSPEncoder
from protocol.hsp_parser import HSPParser


HOST = "127.0.0.1"
PORT = 6379


client = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client.connect((HOST, PORT))

parser = HSPParser()


while True:

    text = input("Hodor> ")

    # Exit client
    if text.lower() == "exit":
        break

    # Ignore empty input
    if not text.strip():
        continue

    try:
        # Convert command line into arguments.
        #
        # SET name "Riju Paul"
        #
        # becomes:
        #
        # ["SET", "name", "Riju Paul"]

        tokens = shlex.split(text)

    except ValueError as e:

        print("Syntax error:", e)
        continue

    if not tokens:
        continue

    # Convert command into HSP
    request = HSPEncoder.array(tokens)

    print("Sending:", request)

    # Send HSP bytes to server
    client.sendall(request)

    # Receive response
    while True:

        data = client.recv(1024)

        if not data:

            print("Server disconnected")
            client.close()
            exit()

        # Parse received HSP response
        responses = parser.feed(data)

        # Response is incomplete
        if not responses:
            continue

        for response in responses:

            print("Response:", response)

        break


client.close()